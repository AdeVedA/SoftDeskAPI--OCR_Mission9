from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ContributorViewSet, IssueViewSet, ProjectViewSet

# Crée un routeur qui gère les routes automatiquement pour chaque ViewSet
router = DefaultRouter()

# Enregistre le ViewSet pour les projets
router.register(r"", ProjectViewSet, basename="project")
# Enregistre le ViewSet pour les contributeurs, avec project en paramètre d'URL
router.register(r"(?P<project>\d+)/contributors", ContributorViewSet, basename="contributor")
# Enregistre le ViewSet pour les issues, avec project en paramètre d'URL
router.register(r"(?P<project>\d+)/issues", IssueViewSet, basename="issue")
# Enregistre le ViewSet pour les commentaires, avec project et issue en paramètres d'URL
router.register(r"(?P<project>\d+)/issues/(?P<issue>\d+)/comments", CommentViewSet, basename="comment")
# Utilise les URLs générées automatiquement par le routeur
urlpatterns = [
    path("", include(router.urls)),
]
