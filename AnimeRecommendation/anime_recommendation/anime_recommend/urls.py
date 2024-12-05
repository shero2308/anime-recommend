from django.urls import path 
from .views import RegisterView, LoginView, AnimeSearchView, RecommendationsView, PreferencesView

urlpatterns = [
    path('auth/register', RegisterView.as_view(),name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('anime/search', AnimeSearchView.as_view(), name='anime_search'),
    path('anime/recommendations', RecommendationsView.as_view(), name='recommendations'),
    path('user/preferences', PreferencesView.as_view(), name='preferences'),
]

