from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import User, anime_data
from .serializer import UserSerializer, AnimeSerializer
import requests
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class AnimeSearchView(APIView):
    def get(self, request):
        name = request.query_params.get("name")
        genre = request.query_params.get("genre")

        query = """
        query ($name: String, $genre: String) {
            Page {
                media(search: $name, genre: $genre, type: ANIME) {
                    id
                    title { romaji }
                    genres
                    popularity
                }
            }
        }
        """
        variables = {"name": name, "genre": genre}
        try:
            response = requests.post(
                "https://graphql.anilist.co",
                json={"query": query, "variables": variables},
                timeout=10
            )
            response.raise_for_status()
            data = response.json().get("data", {}).get("Page", {}).get("media", [])
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class RecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        preferences = user.anime_liking.get("genres", [])
        if not preferences:
            return Response({"message": "No preferences found for recommendations."}, status=status.HTTP_404_NOT_FOUND)
        
        recommended_anime = anime_data.objects.filter(
            genre__overlap=preferences
        ).order_by('-popularity')

        if not recommended_anime.exists():
            return Response({"message": "No recommendations available."}, status=status.HTTP_204_NO_CONTENT)

        serializer = AnimeSerializer(recommended_anime, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PreferencesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(request.user.anime_liking, status=status.HTTP_200_OK)

    def post(self, request):
        preferences = request.data.get("genres", [])
        if not isinstance(preferences, list) or not all(isinstance(genre, str) for genre in preferences):
            return Response({"error": "Invalid preferences format. Expecting a list of genres."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.anime_liking = {"genres": preferences}
        request.user.save()
        return Response({"message": "Preferences updated successfully!"}, status=status.HTTP_200_OK)
