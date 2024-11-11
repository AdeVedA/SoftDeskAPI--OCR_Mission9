from rest_framework.permissions import BasePermission

from .models import Contributor


class IsAuthorOrReadOnly(BasePermission):
    """La permission permet à l'auteur d'une ressource de la modifier ou de la supprimer.
    Tous les autres utilisateurs peuvent seulement lire la ressource.
    """

    def has_object_permission(self, request, view, obj):
        # Permissions de lecture sont autorisées pour tous
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Seul l'auteur peut modifier ou supprimer
        return obj.author == request.user


class IsContributor(BasePermission):
    """Permission qui vérifie que l'utilisateur est contributeur d'un projet pour y accéder."""

    def has_permission(self, request, view):
        # Pour les vues de liste (GET /projects/), le `get_queryset` de la vue gère le filtrage des projets visibles
        if view.action == "list":
            return True

        # Pour les vues de détail (avec project_id), vérifier ici que l'utilisateur est contributeur du projet
        project_id = view.kwargs.get("project")
        if project_id:
            return Contributor.objects.filter(project_id=project_id, user=request.user).exists()

        # Pour d'autres types de requêtes, laisser les autres permissions décider
        return True
