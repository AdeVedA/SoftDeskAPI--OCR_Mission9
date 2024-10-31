from django.db import models
from django.conf import settings
import uuid


class Project(models.Model):
    """modèle pour représenter un projet
    (author, name, description, type, created_time)
    """
    TYPE_CHOICES = [
            ('back-end', 'Back End'),
            ('front-end', 'Front End'),
            ('iOS', 'iOS'),
            ('Android', 'Android')
        ]
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_author')
    name = models.CharField(
        max_length=255, verbose_name="Nom du projet")
    description = models.TextField(
        max_length=4095, verbose_name="description du projet")
    type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, default='back-end')
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création")


class Contributor(models.Model):
    """modèle pour représenter un contributeur,
    classe de liaison many-to-many entre User et Project
    (user, project, role=CONTRIBUTOR(default), AUTHOR)
    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contribute_to')
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name='contributed_by')
    author = models.BooleanField(
        default=False)

    class Meta:
        unique_together = ('user', 'project')


class Issue(models.Model):
    """modèle pour représenter une tâche/difficulté/fonctionnalité
    (project, author, name, description,
    priority, tag, status, attribution, created_time)
    """
    PRIORITY_CHOICES = [
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High')
        ]
    TAG_CHOICES = [
            ('Bug', 'Bug'),
            ('Feature', 'Feature'),
            ('Task', 'Task')
        ]
    STATUS_CHOICES = [
            ('to-do', 'To Do'),
            ('in-progress', 'In Progress'),
            ('finished', 'Finished')
        ]

    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='issue_author')
    name = models.CharField(
        max_length=127, verbose_name="Intitulé de la question")
    description = models.TextField(
        max_length=1023, verbose_name="description de la tâche")
    priority = models.CharField(
        max_length=6, choices=PRIORITY_CHOICES,
        default='Low', verbose_name="priorité de la tâche")
    tag = models.CharField(
        max_length=8, choices=TAG_CHOICES,
        default='Bug', verbose_name="type de la tâche")
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES,
        default='to-do', verbose_name="status de la tâche")
    attribution = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création de la tâche")


class Comment(models.Model):
    """modèle pour représenter un commentaire
    (issue, author, description, uuid, created_time)
    """
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_author')
    description = models.TextField(
        max_length=4095, verbose_name="contenu du commentaire")
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True,
        verbose_name="identifiant numérique du commentaire")
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création du commentaire")
