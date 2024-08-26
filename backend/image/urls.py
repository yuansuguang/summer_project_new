from django.urls import path
from . import views

urlpatterns = [
    path('api/upload_image', views.upload_image, name='upload_image'),
]