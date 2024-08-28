from django.urls import path
from . import views

urlpatterns = [
    path('api/getoptions/<int:question_id>', views.get_options, name='get_options')
]