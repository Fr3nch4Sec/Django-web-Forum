from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Sujet, Message, Category, Like, Notification, Tag
from .forms import SujetForm, MessageForm
from django.db.models import Q
from django.core.paginator import Paginator
import json


def sujet_list(request):
    query = request.GET.get('q', '')
    sujets = Sujet.objects.all().order_by('-date_creation')
    if query:
        sujets = sujets.filter(Q(titre__icontains=query))
    paginator = Paginator(sujets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'query': query,
        'unread_notifications': Notification.objects.filter(utilisateur=request.user, lu=False).count() if request.user.is_authenticated else 0
    }
    return render(request, 'discussion/sujet_list.html', context)

def sujet_detail(request, pk):
    sujet = get_object_or_404(Sujet, pk=pk)
    messages = sujet.messages.all()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sujet = sujet
            message.auteur = request.user
            message.save()
            content = form.cleaned_data['contenu']
            usernames = {word[1:] for word in content.split() if word.startswith('@') and len(word) > 1}
            for username in usernames:
                try:
                    user = User.objects.get(username=username)
                    Notification.objects.get_or_create(utilisateur=user, message=message)
                except User.DoesNotExist:
                    pass
            return redirect('sujet_detail', pk=sujet.pk)
    else:
        form = MessageForm()
    context = {
        'sujet': sujet,
        'messages': messages,
        'form': form,
        'unread_notifications': Notification.objects.filter(utilisateur=request.user, lu=False).count() if request.user.is_authenticated else 0
    }
    return render(request, 'discussion/sujet_detail.html', context)

@login_required
def sujet_create(request):
    if request.method == 'POST':
        form = SujetForm(request.POST)
        if form.is_valid():
            sujet = form.save(commit=False)
            sujet.auteur = request.user
            sujet.save()
            form.save_m2m()
            return redirect('sujet_list')
    else:
        form = SujetForm()
    context = {
        'form': form,
        'unread_notifications': Notification.objects.filter(utilisateur=request.user, lu=False).count() if request.user.is_authenticated else 0
    }
    return render(request, 'discussion/sujet_create.html', context)

@login_required
def like_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    like, created = Like.objects.get_or_create(message=message, utilisateur=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'like_count': message.likes.count()})

@login_required
def notifications(request):
    notifications = Notification.objects.filter(utilisateur=request.user).order_by('-date_creation')
    unread = notifications.filter(lu=False)
    unread.update(lu=True)
    context = {
        'notifications': notifications,
        'unread_notifications': 0
    }
    return render(request, 'discussion/notifications.html', context)

@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, utilisateur=request.user)
    if request.method == 'POST':
        notification.delete()
        return redirect('notifications')
    context = {
        'notification': notification,
        'unread_notifications': Notification.objects.filter(utilisateur=request.user, lu=False).count()
    }
    return render(request, 'discussion/notification_confirm_delete.html', context)

@login_required
def toggle_dark_mode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.session['dark_mode'] = data.get('dark_mode', False)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

def sujet_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, nom=tag_name)
    sujets = Sujet.objects.filter(tags=tag).order_by('-date_creation')
    paginator = Paginator(sujets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'tag': tag,
        'unread_notifications': Notification.objects.filter(utilisateur=request.user, lu=False).count() if request.user.is_authenticated else 0
    }
    return render(request, 'discussion/sujet_list.html', context)