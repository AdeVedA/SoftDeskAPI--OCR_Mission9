from projects.models import Project
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serialisation/déserialisation pour la création/mise à jour des instances du modèle User"""

    date_joined = serializers.ReadOnlyField()
    can_be_contacted = serializers.BooleanField(default=True)
    can_data_be_shared = serializers.BooleanField(default=False)

    class Meta(object):
        model = User
        fields = (
            "id",
            "username",
            "age",
            "email",
            "password",
            "date_joined",
            "can_be_contacted",
            "can_data_be_shared",
        )
        # mot de passe jamais renvoyé dans les réponses de l'API
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Récupère et supprime le mot de passe des données validées
        password = validated_data.pop("password")
        # Crée une instance de l'utilisateur avec les données restantes (sans le mot de passe)
        user = User(**validated_data)
        # Définit le mot de passe en utilisant la méthode set_password()
        # qui hache automatiquement le mot de passe avant de le stocker
        user.set_password(password)
        # Sauvegarde l'utilisateur dans la base de données
        user.save()
        # Retourne l'utilisateur nouvellement créé
        return user


class UserListSerializer(serializers.ModelSerializer):
    """gérer l'affichage par liste des utilisateurs avec respect des choix de confidentialité"""

    email = serializers.SerializerMethodField()
    projects_contributed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "projects_contributed"]

    def get_email(self, obj):
        # Affiche l'email seulement si can_be_contacted est True
        return obj.email if obj.can_be_contacted else None

    def get_projects_contributed(self, obj):
        # Récupère les noms des projets où l'utilisateur est contributeur
        if obj.can_data_be_shared:
            projects_contributed = Project.objects.filter(contributed_by__user=obj).values_list("name", flat=True)
            return list(projects_contributed)
        return []


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """gérer la validation et la génération des tokens JWT"""

    def validate(self, attrs):
        try:
            # Authentifie l'utilisateur via l'email
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Email non valide.")

        if not user.check_password(attrs["password"]):
            raise serializers.ValidationError("Mot de passe incorrect.")

        data = super().validate(attrs)
        data["user_details"] = {
            "username": user.username,
            "email": user.email,
        }
        return data
