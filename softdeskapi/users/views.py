from django.shortcuts import get_object_or_404
from projects.models import Project
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import CustomTokenObtainPairSerializer, UserListSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Vue pour gérer les opérations CRUD sur le modèle User (pour le RGPD...)."""

    queryset = User.objects.all().order_by("id")  # ordonner les users par id pour une pagination cohérente
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # Utilise `UserListSerializer` pour les requêtes en lecture seule (GET)
        # et `UserSerializer` pour la création/mise à jour (POST)
        if self.action in ["list", "retrieve"]:
            return UserListSerializer
        return UserSerializer

    def get_queryset(self):
        return self.queryset

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "Use /delete_account/ endpoint to delete user."}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=True, methods=["get"])
    def contact_info(self, request, pk=None):
        """Renvoie l'email et les projets si conditions `can_be_contacted` et `can_data_be_shared` sont remplies."""
        user = self.get_object()
        response_data = {}

        if user.can_be_contacted:
            response_data["email"] = user.email

        if user.can_data_be_shared:
            projects = Project.objects.filter(contributed_by__user=user)
            response_data["projects"] = [{"id": project.id, "name": project.name} for project in projects]

        return Response(response_data)

    @action(detail=True, methods=["delete"])
    def delete_account(self, request, pk=None):
        """Vérifie si l'utilisateur est auteur de contenus avant de supprimer le compte."""
        user = self.get_object()

        # Vérifier si l'utilisateur a des contenus liés
        has_authored_content = (
            user.project_author.exists() or user.issue_author.exists() or user.comment_author.exists()
        )

        # Si il y en a, demander
        if has_authored_content:
            return Response(
                {
                    "detail": "You have authored contents.",
                    "options": {
                        "delete_account_and_contents": "Delete your account and all authored contents.",
                        "cancel": "Cancel deletion. Remove your contents manually before trying again.",
                    },
                },
                status=status.HTTP_200_OK,
            )

        user.delete()
        return Response({"detail": "User account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def confirm_delete_account(self, request, pk=None):
        """Supprime le compte utilisateur et tous les contenus associés."""
        user = self.get_object()
        if "delete_account_and_contents" in request.data:
            user.project_author.all().delete()
            user.issue_author.all().delete()
            user.comment_author.all().delete()
            user.delete()
            return Response(
                {"detail": "User account and all authored contents deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            {"detail": "Deletion cancelled. Please manage your contents before deleting the account."},
            status=status.HTTP_200_OK,
        )


class CreateUserAPIView(APIView):
    """Cette classe gère la création d'un utilisateur via l'API"""

    # Permission qui permet à tout utilisateur (authentifié ou non) d'accéder à cette URL
    permission_classes = (AllowAny,)
    authentication_classes = []  # Désactive l'authentification pour cette vue

    def post(self, request):
        # Crée un sérialiseur en passant les données reçues dans la requête (request.data)
        serializer = UserSerializer(data=request.data)
        # Vérifie si les données sont valides selon les règles définies dans le sérialiseur
        if serializer.is_valid():
            # Si valide, sauvegarde l'utilisateur en base de données
            serializer.save()
            # Renvoie les données de l'utilisateur créé et un code de statut HTTP 201 (Créé)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Si les données sont invalides, renvoie les erreurs avec un code 400 (Mauvaise requête)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """sous-classe de TokenObtainPairView (rest_framework_simplejwt) qui personnalise
    la réponse lors de l'obtention des tokens JWT d'accès et de rafraîchissement
    Args:
        TokenObtainPairView (parent class):
        permettre aux utilisateurs d'obtenir des tokens JWT (d'accès et de rafraîchissement)
    """

    serializer_class = CustomTokenObtainPairSerializer

    # Reçoit une requête POST avec les informations de connexion (comme l'email et le mot de passe)
    def post(self, request, *args, **kwargs):
        # Appelle la méthode POST de la vue parent (TokenObtainPairView) pour générer le token
        response = super().post(request, *args, **kwargs)
        # Récupère l'utilisateur correspondant à l'email fourni dans la requête
        user = get_object_or_404(User, email=request.data["email"])
        # Crée un dictionnaire avec les détails de l'utilisateur (nom d'utilisateur et email)
        user_details = {
            "username": user.username,
            "email": user.email,
            "date_joined": user.date_joined,
        }
        # Retourne la réponse avec le token d'accès, le token de rafraîchissement,
        # et les détails de l'utilisateur, avec un code de statut HTTP 200 (Succès)
        return Response(
            {
                "token": response.data["access"],  # Token d'accès JWT pour accéder aux ressources sécurisées
                "refresh": response.data["refresh"],  # Token de rafraîchissement JWT pour renouveler le token d'accès
                "user_details": user_details,  # Détails supplémentaires de l'utilisateur pour personnaliser la réponse
            },
            status=status.HTTP_200_OK,
        )
