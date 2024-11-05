# users/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.utils import timezone


class UserManager(BaseUserManager):
    """Gestionnaire de modèle personnalisé pour créer et enregistrer des utilisateurs."""

    def _create_user(self, email, password, **extra_fields):
        """Crée et enregistre un utilisateur avec l'email et le mot de passe donnés.
        Cette méthode privée est utilisée par create_user et create_superuser.
        """
        if not email:
            raise ValueError("L'Email doit être renseigné")
        try:
            # s'assurer avec une transaction atomique que les opérations de ce bloc
            # ne soient effectives que si elles réussissent toutes
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except Exception as e:
            raise e

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        if "age" not in extra_fields:
            raise ValueError("L'âge doit être renseigné")
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """modèle d'utilisateur personnalisé avec des champs supplémentaires."""

    username = models.CharField(max_length=30, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(120)])
    email = models.EmailField(max_length=40, unique=True)
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "age"]

    def save(self, *args, **kwargs):
        """Enregistre l'utilisateur dans la base de données."""
        super().save(*args, **kwargs)
