from rest_framework.permissions import BasePermission


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
