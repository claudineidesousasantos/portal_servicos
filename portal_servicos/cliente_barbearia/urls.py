from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'cliente_barbearia'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='cliente_barbearia/login.html'), name='login'),
    path('funcionario/<int:funcionario_id>/agendar/', views.agendar, name='agendar'),
]
