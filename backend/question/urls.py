from django.urls import path
from . import views

urlpatterns = [
    path('api/listquestion', views.list_question, name='list_question'),
    path('api/list_question_for_fill', views.list_question_forfill, name='list_question_forfill'),
    path('api/listquestionalt', views.list_question_alt, name='list_question_alt'),
    path('api/listquestionforpreview', views.list_question_forpreview, name='list_question_forpreview'),
    path('api/listquestionforanalysis', views.list_question_foranalysis, name='list_question_foranalysis'),
    path('api/getquestions/<int:survey_id>', views.get_questions, name='get_questions'),
    path('api/getdetails/<int:question_id>', views.get_details, name='get_details'),
    path('api/getoptions/<int:question_id>', views.get_options, name='get_options')
]