from django.urls import path
from . import views

urlpatterns = [
    path('api/submit_survey', views.submit_survey, name='submit_survey'),
    path('api/save_survey', views.save_survey, name='save_survey'),
    path('api/clear_survey', views.clear_survey, name='clear_survey'),
    path('api/get_submissions_by_question_id', views.get_submissions_by_question_id, name='get_submissions_by_question_id'),
    path('api/get_question_statistics', views.get_question_statistics, name='get_question_statistics'),
    path('api/get_survey_submissions', views.get_survey_submissions, name='get_survey_submissions'),
    path('api/get_user_submissions', views.get_user_submissions, name='get_user_submissions'),
    path('api/delete_submission', views.delete_submission, name='delete_submission')
]

