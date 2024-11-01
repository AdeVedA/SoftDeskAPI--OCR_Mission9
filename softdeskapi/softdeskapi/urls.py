from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from projects.views import ProjectViewSet
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

# Initialise DefaultRouter pour offrir une vue structurée sur la racine
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")  # Base URL "/users/"
router.register(r"projects", ProjectViewSet, basename="project")  # Base URL "/projects/"

urlpatterns = [
    path("admin/", admin.site.urls),
    # Inclut les URL de base générées par DefaultRouter
    path("", include(router.urls)),
    # Inclut les URLs supplémentaires de l'application users
    path("users/", include("users.urls")),
    # Inclut les URLs supplémentaires de l'application projects
    path("projects/", include("projects.urls")),
]
