from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reserva/<int:gift_id>/', views.reserve_gift, name='reserve_gift'),
    
    # Custom Admin Panel
    path('painel/', views.panel_dashboard, name='panel_dashboard'),
    path('painel/presentes/novo/', views.panel_gift_create, name='panel_gift_create'),
    path('painel/presentes/<int:pk>/editar/', views.panel_gift_edit, name='panel_gift_edit'),
    path('painel/presentes/<int:pk>/excluir/', views.panel_gift_delete, name='panel_gift_delete'),
]
