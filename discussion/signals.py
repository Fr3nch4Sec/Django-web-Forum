# discussion/signals.py (créer ce fichier si absent)
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification
from django.contrib.auth.models import User
import re

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Rechercher les mentions @utilisateur dans le contenu
        mentions = re.findall(r'@(\w+)', instance.contenu)
        for mention in mentions:
            try:
                utilisateur = User.objects.get(username=mention)
                Notification.objects.create(
                    utilisateur=utilisateur,
                    message=instance,
                    contenu=f"Vous avez été mentionné dans un message de {instance.auteur} dans le sujet '{instance.sujet.titre}'."
                )
            except User.DoesNotExist:
                pass