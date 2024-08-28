from django.shortcuts import render
from django.http import JsonResponse
# from captcha.models import CaptchaStore
# from captcha.helpers import captcha_image_url
from survey.models import *
from utils.hashcode import *
from django.views.decorators.csrf import csrf_exempt
from survey.form import *

import json

@csrf_exempt
def survey_list(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        # survey_id = request.POST.get('survey_id')
        # print("enter")
        survey_form = list_survey_form(request.POST)
        if survey_form.is_valid():
            survey_keyword = survey_form.cleaned_data.get('survey_keyword')
            is_deleted = survey_form.cleaned_data.get('is_deleted')
            is_collected = survey_form.cleaned_data.get('is_collected')
            is_released = survey_form.cleaned_data.get('is_released')
            survey_type = survey_form.cleaned_data.get('survey_type')

            sort_key = survey_form.cleaned_data.get('sort_key')
            sort_type = survey_form.cleaned_data.get('sort_type')

            # username = survey_form.cleaned_data.get('username')
            username = request.session.get('username')

            print(username)
            print(is_released)

            if sort_key is None:
                sort_key = "last_modified_time"
            if sort_type is None:
                sort_type = "desc"

            survey_list = Survey.objects.filter(username=username)
            print(survey_list)
            if is_deleted:
                survey_list = survey_list.filter(is_deleted=True)
            else:
                survey_list = survey_list.filter(is_deleted=False)
            print("checkpoint 1")
            if survey_keyword:
                survey_list = survey_list.filter(survey_title__contains=survey_keyword)
            if is_collected:
                survey_list = survey_list.filter(is_collected=True)
            print(survey_list)
            # else:
            #     survey_list = survey_list.filter(is_collected=False)
            if is_released == 1:
                print("enter here")
                survey_list = survey_list.filter(is_available=True)
            elif is_released == 2:
                survey_list = survey_list.filter(is_available=False)
            if survey_type:
                survey_list = survey_list.filter(survey_type=survey_type)
            # if sort_type == 'desc':
            #     survey_list = survey_list.order_by('-' + sort_key)
            # else:
            #     survey_list = survey_list.order_by(sort_key)
            
            print("checkpoint 2")
            
            response = []
            for survey in survey_list:
                item = {"questionnaireId": survey.survey_id,
                        "questionnaireName": survey.survey_title, 
                        "isPublished": survey.is_available,
                        "is_deleted": survey.is_deleted,
                        "is_collected": survey.is_collected,
                        "answersCount": survey.submission_num,
                        "question_num": survey.question_num,
                        "questionType": survey.survey_type,
                        "creationDate": survey.create_time.strftime("%Y-%m-%d %H:%M"),
                        "last_modified_time": survey.last_modified_time.strftime("%Y-%m-%d %H:%M"),
                        "deadline": survey.deadline,
                        "duration": survey.duration}
                response.append(item)
            
            if response:
                return JsonResponse({'status_code': 1, 'data': json.dumps(response, ensure_ascii=False)})
            else:
                return JsonResponse({'status_code': 2, 'message': r'no result'})
        else:
            return JsonResponse({'status_code': 4, 'message': r'invalid form'})
        
    else:
        return JsonResponse({'status_code': 3, 'message': r'something went wrong...'})



@csrf_exempt
def survey_share(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        shareform = share_survey_form(request.POST)
        if shareform.is_valid():
            survey_id = shareform.cleaned_data.get('survey_id')
            try:
                survey = Survey.objects.get(survey_id=survey_id)
            except:
                return JsonResponse({'status_code': 2, 'message': r'survey not exists'})
            
            username = survey.username
            code = hashcode(username, str(survey_id))

            survey.is_available = True
            survey.share_code = code
            survey.save()

            return JsonResponse({'status_code': 1, 'code': code})
        else:
            return JsonResponse({'status_code': 3, 'message': r'invalid form'})
    else:
        return JsonResponse({'status_code': 4, 'message': r'method error'})


@csrf_exempt
def survey_link(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        shareform = share_survey_form(request.POST)
        if shareform.is_valid():
            survey_id = shareform.cleaned_data.get('survey_id')
            try:
                survey = Survey.objects.get(survey_id=survey_id)
            except:
                return JsonResponse({'status_code': 2, 'message': r'survey not exists'})
            
            if survey.is_available == False:
                return JsonResponse({'status_code': 5, 'message': r'not available'})

            return JsonResponse({'status_code': 1, 'code': survey.share_code})
        else:
            return JsonResponse({'status_code': 3, 'message': r'invalid form'})
    else:
        return JsonResponse({'status_code': 4, 'message': r'method error'})
        

# Create your views here.

#获取问卷信息接口
@csrf_exempt
def get_survey_detail(request, survey_id):
    # if not request.session.get('is_login'):
    #     return JsonResponse({'status_code': 401})
    
    if request.method == 'GET':
        try:
            survey = Survey.objects.get(survey_id = survey_id)
            survey_data = {
                "survey_id": survey.survey_id,
                "survey_title": survey.survey_title,
                "survey_description": survey.survey_description,
                "survey_type": survey.survey_type,
                "survey_code": survey.share_code,
                "submission_num": survey.submission_num,
                "survey_deadline": survey.deadline,
            }
            return JsonResponse(survey_data)
        
        except Survey.DoesNotExist:
            return JsonResponse({'status_code': 2, 'message': r'Survey not found.'})

#通过share code获取问卷信息接口
@csrf_exempt
def get_survey_detail_code(request, share_code):
    # if not request.session.get('is_login'):
    #     return JsonResponse({'status_code': 401})
    
    if request.method == 'GET':
        try:
            survey = Survey.objects.get(share_code = share_code)
            survey_data = {
                "survey_id": survey.survey_id,
                "survey_title": survey.survey_title,
                "survey_description": survey.survey_description,
                "survey_type": survey.survey_type,
                "survey_code": survey.share_code,
                "submission_num": survey.submission_num,
                "survey_deadline": survey.deadline,
                "max_submission_num": survey.max_submission
            }
            return JsonResponse(survey_data)
        
        except Survey.DoesNotExist:
            return JsonResponse({'status_code': 2, 'message': r'Survey not found.'})
        
@csrf_exempt
def add_submission(request, survey_id):
    # if not request.session.get('is_login'):
    #     return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        try:
            survey = Survey.objects.get(survey_id = survey_id)
            survey.submission_num += 1
            survey.save()
            return JsonResponse({'status_code': 1, 'message': r'add success.', 'current_num': survey.submission_num})
        
        except Survey.DoesNotExist:
            return JsonResponse({'status_code': 2, 'message': r'Survey not found.'})
        
@csrf_exempt
def clear_submission(request, survey_id):
    # if not request.session.get('is_login'):
    #     return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        try:
            survey = Survey.objects.get(survey_id = survey_id)
            survey.submission_num = 0
            survey.save()
            return JsonResponse({'status_code': 1, 'message': r'add success.', 'current_num': survey.submission_num})
        
        except Survey.DoesNotExist:
            return JsonResponse({'status_code': 2, 'message': r'Survey not found.'})