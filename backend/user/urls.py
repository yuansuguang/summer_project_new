from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register, name='register'),
    path('confirm/', views.user_confirm, name='user_confirm'),  
    path('api/login/', views.login, name='login'),
    path('api/logout/', views.logout, name='logout'),
    path('api/userinfo/', views.get_user_info, name='get_user_info'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_confirm/<str:code>/', views.reset_password_confirm, name='reset_password_confirm')   
]