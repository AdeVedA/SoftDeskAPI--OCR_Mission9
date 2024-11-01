from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Comment, Contributor, Issue, Project


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ["id", "author", "name", "description", "type", "created_time"]
        read_only_fields = ["id", "author"]

    def create(self, validated_data):
        # Création d'un projet avec ajout automatique de l'auteur comme contributeur
        project = Project.objects.create(**validated_data)
        Contributor.objects.create(user=self.context["request"].user, project=project, author=True)
        return project


class ContributorSerializer(serializers.ModelSerializer):
    # Projet en lecture seule pour éviter d'avoir à renseigner dans le body ce qui est déjà dans l'url
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Contributor
        fields = ["id", "user", "project", "author"]

    def validate(self, data):
        # récupérer le projet par l'url
        project = self.context["view"].kwargs.get(self.context["view"].lookup_url_kwarg)
        # Vérifie que le contributeur n'est pas déjà dans le projet
        if Contributor.objects.filter(user=data["user"], project=project).exists():
            raise serializers.ValidationError("Cet utilisateur est déjà contributeur de ce projet.")
        return data


class IssueSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=False)

    class Meta:
        model = Issue
        fields = [
            "id",
            "project",
            "author",
            "name",
            "description",
            "priority",
            "tag",
            "status",
            "attribution",
            "created_time",
        ]

    def create(self, validated_data):
        # Associe l'issue au projet en contexte
        project_id = self.context["view"].kwargs.get("project")
        project = get_object_or_404(Project, id=project_id)
        validated_data["project"] = project
        return super().create(validated_data)

    def validate(self, data):
        # Validation pour s'assurer que
        # le contributeur assigné est bien un contributeur du projet.
        project_id = self.context["view"].kwargs.get("project")
        if not Contributor.objects.filter(project_id=project_id, user=data["attribution"]).exists():
            raise serializers.ValidationError("L'utilisateur assigné doit être un contributeur de ce projet.")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ["id", "issue", "author", "description", "uuid", "created_time"]
