from django.contrib import admin
from .models import Sujet, Message, Category, Like, Notification, Tag

admin.site.register(Sujet)
admin.site.register(Message)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Notification)
admin.site.register(Tag)