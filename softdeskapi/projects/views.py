from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Comment, Contributor, Issue, Project
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, ContributorSerializer, IssueSerializer, ProjectSerializer


class ProjectPagination(PageNumberPagination):
    """Pagination personnalisée pour limiter le nombre d'éléments par page."""

    page_size = 10  # nombre maximum d'éléments par page


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les opérations CRUD sur les projets.
    Seuls les auteurs peuvent modifier ou supprimer les projets,
    mais tous les utilisateurs authentifiés peuvent lire et créer des projets.
    """

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = ProjectPagination

    def get_queryset(self):
        """
        Récupère la liste des projets auxquels l'utilisateur est contributeur.
        Si un ID de projet est spécifié dans l'URL, vérifie que l'utilisateur est contributeur aussi.
        """
        # Récupérer l'ID du projet depuis les paramètres de l'URL ("pk" pour les routes détails project/1/)
        project_id = self.kwargs.get("pk")

        # Si un ID de projet est spécifié, l'utilisateur doit être contributeur du projet
        if project_id:
            if Contributor.objects.filter(project_id=project_id, user=self.request.user).exists():
                return Project.objects.filter(id=project_id).select_related("author")
            raise PermissionDenied("Vous devez être contributeur de ce projet pour accéder à ses détails.")

        # Si aucun ID spécifique n'est précisé, renvoie tous les projets auxquels l'utilisateur est contributeur
        return Project.objects.filter(contributed_by__user=self.request.user).select_related("author")

    def perform_create(self, serializer):
        """
        l'utilisateur qui crée un projet est automatiquement défini comme auteur et contributeur du projet.
        Si cet utilisateur n'est pas encore contributeur, il est ajouté avec le statut d'auteur.
        """
        # Sauvegarde du projet avec l'utilisateur actuel comme auteur
        project = serializer.save(author=self.request.user)
        # Ajoute l'utilisateur comme contributeur, s'il ne l'est pas déjà
        if not Contributor.objects.filter(user=self.request.user, project=project).exists():
            Contributor.objects.create(user=self.request.user, project=project, author=True)


class ContributorViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les contributeurs d'un projet.
    Seuls les utilisateurs authentifiés peuvent ajouter et lire les contributeurs d'un projet.
    """

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ProjectPagination

    def get_queryset(self):
        """Récupère tous les contributeurs pour un projet donné.
        Filtre les contributeurs en fonction de l'ID du projet spécifié dans l'URL.
        """
        # Récupère les contributeurs associés à un projet spécifique
        return Contributor.objects.select_related("user", "project").filter(project__id=self.kwargs["project"])

    def perform_create(self, serializer):
        """Ajoute un contributeur à un projet. Vérifie d'abord que l'utilisateur actuel
        n'est pas déjà contributeur. Lève une exception si l'utilisateur est déjà dans le projet.
        """
        # Récupère le projet avec l'ID passé dans les paramètres d'URL
        project = Project.objects.get(id=self.kwargs["project"])

        # Vérifie que l'utilisateur actuel n'est pas déjà contributeur
        if Contributor.objects.filter(user=self.request.user, project=project).exists():
            raise PermissionDenied("Vous êtes déjà contributeur de ce projet.")
        # Vérifie que l'utilisateur spécifié n'est pas déjà contributeur du projet
        if Contributor.objects.filter(user=serializer.validated_data["user"], project=project).exists():
            raise PermissionDenied("Cet utilisateur est déjà contributeur de ce projet.")
        # Enregistre le contributeur en liant le projet et l'utilisateur actuel
        serializer.save(project=project, user=self.request.user)


class IssueViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les issues dans un projet.
    Seuls les auteurs d'une issue peuvent la modifier ou la supprimer,
    mais tous les utilisateurs authentifiés peuvent lire et créer des issues.
    """

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = ProjectPagination

    def get_queryset(self):
        """Récupère toutes les issues pour un projet donné auquel l'utilisateur est contributeur.
        Filtre les issues en fonction de l'ID du projet spécifié dans l'URL et de l'appartenance
        de l'utilisateur au projet.
        """
        # Récupère l'ID du projet depuis les paramètres de l'URL
        project_id = self.kwargs.get("project")

        # Vérifie si l'utilisateur est contributeur du projet
        if Contributor.objects.filter(project_id=project_id, user=self.request.user).exists():
            return Issue.objects.select_related("author", "project").filter(project__id=project_id)

        # Si l'utilisateur n'est pas contributeur, lève une exception avec un message explicatif
        raise PermissionDenied("Vous devez être contributeur de ce projet pour accéder à ses issues.")

    def get_serializer_context(self):
        """Ajoute le projet dans le contexte du sérialiseur pour permettre
        une liaison facile entre une nouvelle issue et le projet auquel elle appartient.
        """
        context = super().get_serializer_context()
        # Ajoute le projet correspondant au contexte
        context["project"] = get_object_or_404(Project, id=self.kwargs["project"])
        return context


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les commentaires sur une issue spécifique.
    Seuls les auteurs d'un commentaire peuvent le modifier ou le supprimer,
    mais tous les utilisateurs authentifiés peuvent lire et créer des commentaires.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = ProjectPagination

    def get_queryset(self):
        """Récupère tous les commentaires pour une issue donnée dans un projet auquel l'utilisateur est contributeur.
        Si l'utilisateur n'est pas contributeur, une exception est levée pour indiquer le manque de permissions.
        """
        project_id = self.kwargs.get("project")
        issue_id = self.kwargs.get("issue")

        # Vérifie si l'utilisateur est contributeur du projet
        if Contributor.objects.filter(project_id=project_id, user=self.request.user).exists():
            return Comment.objects.select_related("author", "issue").filter(
                issue__id=issue_id, issue__project__id=project_id
            )

        # Si l'utilisateur n'est pas contributeur, lève une exception avec un message explicatif
        raise PermissionDenied("Vous devez être contributeur de ce projet pour accéder à ses commentaires.")

    def perform_create(self, serializer):
        """Crée un commentaire lié à une issue spécifique. Vérifie que l'issue
        appartient bien au projet spécifié avant de créer le commentaire.
        """
        # Vérifie que l'issue appartient bien au projet
        try:
            issue = Issue.objects.get(id=self.kwargs["issue"], project__id=self.kwargs["project"])
        except Issue.DoesNotExist:
            # Lève une erreur si l'issue n'appartient pas au projet
            raise serializer.ValidationError("Cette issue n'appartient pas au projet spécifié.")
        # Crée le commentaire en associant l'auteur et l'issue
        serializer.save(author=self.request.user, issue=issue)
