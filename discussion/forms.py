from django import forms
from .models import Sujet, Message, Tag

class SujetForm(forms.ModelForm):
    class Meta:
        model = Sujet
        fields = ['titre', 'categorie', 'tags']
        widgets = {
            'tags': forms.SelectMultiple(attrs={'class': 'form-multiselect'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['contenu']