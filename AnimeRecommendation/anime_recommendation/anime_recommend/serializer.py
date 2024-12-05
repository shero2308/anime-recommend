from rest_framework import serializers
from .models import User, anime_data
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Prevent password from being included in responses

    class Meta:
        model = User
        fields = ['username', 'password', 'anime_liking', 'anime_watched']

    def validate_anime_liking(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Anime liking must be a dictionary.")
        return value

    def validate_anime_watched(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Anime watched must be a list.")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            anime_liking=validated_data.get('anime_liking', {}),
            anime_watched=validated_data.get('anime_watched', []),
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = anime_data
        fields = '__all__'