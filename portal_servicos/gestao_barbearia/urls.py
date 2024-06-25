from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'gestao_barbearia'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('funcionario/<int:funcionario_id>/agenda/', views.visualizar_agenda, name='visualizar_agenda'),
    path('barbearia/<int:barbearia_id>/acessar_cliente_app/', views.acessar_cliente_app, name='acessar_cliente_app'),
    path('funcionario/<int:funcionario_id>/agenda/', views.visualizar_agenda, name='visualizar_agenda'),

]

