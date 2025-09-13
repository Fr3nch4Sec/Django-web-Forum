from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('discussion.urls')),
    path('login/', LoginView.as_view(template_name='discussion/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='discussion/logout.html', next_page='/'), name='logout'),
]