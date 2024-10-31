from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from projects.views import ProjectViewSet

# Initialise DefaultRouter pour offrir une vue structurée sur la racine
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')      # Base URL "/users/"
router.register(r'projects', ProjectViewSet, basename='project')  # Base URL "/projects/"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),         # Inclut les URL de base générées par DefaultRouter
    path('users/', include('users.urls')),  # Inclut les URLs supplémentaires de l'application users
    path('projects/', include('projects.urls')),  # Inclut les URLs supplémentaires de l'application projects
]
