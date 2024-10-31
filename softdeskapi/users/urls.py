from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CreateUserAPIView, CustomTokenObtainPairView

# Initialise DefaultRouter pour les vues basées sur UserViewSet
router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')  # Base URL "/users/"

urlpatterns = [
    path('register/', CreateUserAPIView.as_view(), name='register'),  # Endpoint pour l'inscription
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # authentification JWT
    path('', include(router.urls)),  # Inclut les routes générées par DefaultRouter
]
