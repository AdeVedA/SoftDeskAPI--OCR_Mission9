from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CreateUserAPIView, CustomTokenObtainPairView, UserViewSet

# Initialise DefaultRouter pour les vues basées sur UserViewSet
router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")  # Base URL "/users/"

urlpatterns = [
    # Endpoint pour l'inscription
    path("register/", CreateUserAPIView.as_view(), name="register"),
    # authentification JWT
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Inclut les routes générées par DefaultRouter
    path("", include(router.urls)),
]
