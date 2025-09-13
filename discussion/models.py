from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    nom = models.CharField(max_length=100)
    def __str__(self):
        return self.nom


class Tag(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nom


class Sujet(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre


class Message(models.Model):
    contenu = models.TextField()
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    sujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, related_name='messages')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.auteur} dans {self.sujet}"


class Like(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='likes')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'message')


class Notification(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.utilisateur} sur {self.message}"