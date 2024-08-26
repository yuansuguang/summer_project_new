from django.urls import path
from . import views

urlpatterns = [
    path('api/createsurvey', views.survey_create, name='survey_create'),
    path('api/savesurvey', views.save_entire_survey, name='survey_entire_survey'),
    path('api/openorclosesurvey', views.open_or_close_survey, name='open_or_close_survey'),
    path('api/collectsurvey', views.survey_collect, name='survey_collect'),
    path('api/duplicatesurvey', views.duplicate_survey, name='duplicate_survey'),
    path('api/removetorecycle', views.remove_to_recycle, name='remove_to_recycle'),
    path('api/recoversurvey', views.survey_recover, name='survey_recover'),
    path('api/deletesurvey', views.delete_survey, name='delete_survey')
]