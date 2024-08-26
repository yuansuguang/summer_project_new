from django.shortcuts import render
from django.http import JsonResponse
# from captcha.models import CaptchaStore
# from captcha.helpers import captcha_image_url
from survey.models import *
from utils import hashcode
from django.views.decorators.csrf import csrf_exempt
from survey_manage.form import *
from django.utils import timezone
from django.utils.timezone import make_aware

import json
import datetime


@csrf_exempt
def survey_create(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        survey_form = create_survey_form(request.POST)
        if survey_form.is_valid():
            new_survey = Survey()
            username = request.session.get('username')
            title = survey_form.cleaned_data.get('title')
            description = survey_form.cleaned_data.get('description')
            type = survey_form.cleaned_data.get('type')
            create_time = make_aware(datetime.datetime.now())
            last_modified_time = create_time

            if title == '':
                title = "新建问卷"
            
            if description == '':
                if type == '1':
                    description = "默认简介 1"
                elif type == '2':
                    description = "默认简介 2"
                elif type == '3':
                    description = "默认简介 3"
                else:
                    description = "默认简介 4"
            
            new_survey.survey_title = title
            new_survey.username = username
            new_survey.survey_description = description
            new_survey.survey_type = type
            new_survey.create_time = create_time
            new_survey.last_modified_time = last_modified_time

            new_survey.save()
            return JsonResponse({'status_code': 1, 'survey_id': new_survey.survey_id})
        else:
            return JsonResponse({'status_code': 2, 'message': r'something went wrong with the form'})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


@csrf_exempt
def remove_to_recycle(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        id_form = get_survey_id_form(request.POST)
        if id_form.is_valid():
            survey_id = id_form.cleaned_data.get('survey_id')
            try:
                survey = Survey.objects.get(survey_id=survey_id)
            except:
                return JsonResponse({'status_code': -1, 'message': r'not existing survey'})
            
            survey.is_deleted = True
            survey.save()
            return JsonResponse({'status_code': 1, 'survey_id': survey_id})
        else:
            return JsonResponse({'status_code': 2, 'message': r'something went wrong with the form'})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


@csrf_exempt
def delete_survey(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        id_form = get_survey_id_form(request.POST)
        if id_form.is_valid():
            survey_id = id_form.cleaned_data.get('survey_id')
            try:
                survey = Survey.objects.get(survey_id=survey_id)
            except:
                return JsonResponse({'status_code': -1, 'message': r'not existing survey'})
            
            survey.delete()
            return JsonResponse({'status_code': 1, 'survey_id': survey_id})
        else:
            return JsonResponse({'status_code': 2, 'message': r'something went wrong with the form'})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


@csrf_exempt
def clear_recycle_bin(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'GET':
        username = request.session.get('username')
        survey_list = Survey.objects.filter(username=username, is_deleted=True)
        if survey_list.is_empty():
            return JsonResponse({'status_code': 2, 'message': r'no survey to be deleted'})
        else:
            for survey in survey_list:
                survey.delete()
        return JsonResponse({'status_code': 1})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})



@csrf_exempt
def survey_recover(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        id_form = get_survey_id_form(request.POST)
        if id_form.is_valid():
            survey_id = id_form.cleaned_data.get('survey_id')
            try:
                survey = Survey.objects.get(survey_id=survey_id)
            except:
                return JsonResponse({'status_code': -1, 'message': r'not existing survey'})
            
            survey.is_deleted = False
            survey.save()
            return JsonResponse({'status_code': 1, 'survey_id': survey_id})
        else:
            return JsonResponse({'status_code': 2, 'message': r'something went wrong with the form'})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


@csrf_exempt
def survey_collect(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        id_form = get_survey_id_form(request.POST)
        if id_form.is_valid():
            survey_id = id_form.cleaned_data.get('survey_id')
            try:
                survey = Survey.objects.get(survey_id=survey_id)
            except:
                return JsonResponse({'status_code': -1, 'message': r'not existing survey'})
            
            if survey.is_collected == True:
                survey.is_collected = False
            else:
                survey.is_collected = True
            survey.save()
            return JsonResponse({'status_code': 1, 'survey_id': survey_id})
        else:
            return JsonResponse({'status_code': 2, 'message': r'something went wrong with the form'})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


@csrf_exempt
def publish_survey(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        id_form = get_survey_id_form(request.POST)
        if id_form.is_valid():
            survey_id = id_form.cleaned_data.get('survey_id')
            try:
                survey = Survey.objects.get(survey_id=survey_id)
            except:
                return JsonResponse({'status_code': -1, 'message': r'not existing survey'})
            
            survey.is_available = True
            survey.save()
            return JsonResponse({'status_code': 1, 'survey_id': survey_id})
        else:
            return JsonResponse({'status_code': 2, 'message': r'something went wrong with the form'})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


@csrf_exempt
def close_survey(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        id_form = get_survey_id_form(request.POST)
        if id_form.is_valid():
            survey_id = id_form.cleaned_data.get('survey_id')
            try:
                survey = Survey.objects.get(survey_id=survey_id)
            except:
                return JsonResponse({'status_code': -1, 'message': r'not existing survey'})
            
            survey.is_available = False
            survey.save()
            return JsonResponse({'status_code': 1, 'survey_id': survey_id})
        else:
            return JsonResponse({'status_code': 2, 'message': r'something went wrong with the form'})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


@csrf_exempt
def open_or_close_survey(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        id_form = get_survey_id_form(request.POST)
        if id_form.is_valid():
            survey_id = id_form.cleaned_data.get('survey_id')
            try:
                survey = Survey.objects.get(survey_id=survey_id)
            except:
                return JsonResponse({'status_code': -1, 'message': r'not existing survey'})
            
            if survey.is_available == True:
                survey.is_available = False
            else:
                survey.is_available = True
            survey.save()
            return JsonResponse({'status_code': 1, 'survey_id': survey_id})
        else:
            return JsonResponse({'status_code': 2, 'message': r'something went wrong with the form'})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


    
@csrf_exempt
def update_survey_deadline(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    if request.method == 'POST':
        form = update_survey_deadline_form(request.POST)
        if form.is_valid():
            survey_id = form.cleaned_data.get('survey_id')
            new_deadline = form.cleaned_data.get('new_deadline')
            try:
                survey = Survey.objects.get(survey_id=survey_id)
            except Survey.DoesNotExist:
                return JsonResponse({'status_code': -1, 'message': r'not existing survey'})

            try:
                # 将字符串解析为 datetime 对象
                new_deadline = datetime.datetime.strptime(new_deadline, '%Y-%m-%d %H:%M')
                # 设置时区为当前时区
                new_deadline = timezone.make_aware(new_deadline)
            except ValueError:
                return JsonResponse({'status_code': 2, 'message': r'Invalid date format'})

            survey.deadline = new_deadline
            survey.save()
            return JsonResponse({'status_code': 1, 'survey_id': survey_id})
        else:
            return JsonResponse({'status_code': 3, 'message': r'something went wrong with the form'})
    else:
        return JsonResponse({'status_code': 4, 'message': r'method error'})


@csrf_exempt
def update_survey_duration(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    if request.method == 'POST':
        form = update_survey_duration_form(request.POST)
        if form.is_valid():
            survey_id = form.cleaned_data.get('survey_id')
            new_duration = form.cleaned_data.get('new_duration')
            try:
                survey = Survey.objects.get(survey_id=survey_id)
            except Survey.DoesNotExist:
                return JsonResponse({'status_code': -1, 'message': r'not existing survey'})

            try:
                new_duration = int(new_duration)
                if new_duration <= 0:
                    raise ValueError
            except ValueError:
                return JsonResponse({'status_code': 2, 'message': r'Invalid duration value'})

            survey.duration = new_duration
            survey.save()
            return JsonResponse({'status_code': 1, 'survey_id': survey_id})
        else:
            return JsonResponse({'status_code': 3, 'message': r'something went wrong with the form'})
    else:
        return JsonResponse({'status_code': 4, 'message': r'method error'})


@csrf_exempt
def update_survey_max_submission(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    if request.method == 'POST':
        form = update_survey_max_submission_form(request.POST)
        if form.is_valid():
            survey_id = form.cleaned_data.get('survey_id')
            new_max_submission = form.cleaned_data.get('new_max_submission')
            try:
                survey = Survey.objects.get(survey_id=survey_id)
            except Survey.DoesNotExist:
                return JsonResponse({'status_code': -1, 'message': r'not existing survey'})

            try:
                new_max_submission = int(new_max_submission)
                if new_max_submission <= 0:
                    raise ValueError
            except ValueError:
                return JsonResponse({'status_code': 2, 'message': r'Invalid max submission value'})

            survey.max_submission = new_max_submission
            survey.save()
            return JsonResponse({'status_code': 1, 'survey_id': survey_id})
        else:
            return JsonResponse({'status_code': 3, 'message': r'something went wrong with the form'})
    else:
        return JsonResponse({'status_code': 4, 'message': r'method error'})


@csrf_exempt
def duplicate_survey(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    if request.method == 'POST':
        survey_id = request.POST.get('survey_id')
        try:
            cur_survey = Survey.objects.get(survey_id=survey_id)
        except:
            return JsonResponse({'status_code': 2, 'message': r'survey not found'})
        
        new_survey = Survey()
        new_survey.survey_title = cur_survey.survey_title
        new_survey.survey_description = cur_survey.survey_description
        new_survey.survey_type = cur_survey.survey_type
        new_survey.create_time = make_aware(datetime.datetime.now())
        new_survey.last_modified_time = new_survey.create_time
        new_survey.username = cur_survey.username
        new_survey.deadline = cur_survey.deadline
        new_survey.duration = cur_survey.duration
        new_survey.question_num = cur_survey.question_num

        new_survey.save()

        questions = Question.objects.filter(survey_id=survey_id)
        for cur_question in questions:
            new_question = Question()
            new_question.question_title=cur_question.question_title 
            new_question.question_description=cur_question.question_description
            new_question.survey_id=new_survey
            new_question.question_type=cur_question.question_type
            new_question.is_necessray=cur_question.is_necessary
            new_question.is_hidden=cur_question.is_hidden
            new_question.question_type=cur_question.question_type
            new_question.option_num=cur_question.option_num
            new_question.score=cur_question.score
            new_question.correct_answer=cur_question.correct_answer
            new_question.sequence_id = cur_question.sequence_id
            new_question.max_point = cur_question.max_point

            new_question.save()

            # maybe something to do with sequence_id

            # if cur_question.question_type == 'radio' or cur_question.question_type == 'checkbox':
            cur_options = Option.objects.filter(question_id=cur_question.question_id)
            for option in cur_options:
                new_option = Option()
                new_option.option_description = option.option_description
                new_option.question_id = new_question
                new_option.sequence_id = option.sequence_id
                new_option.save()
            
        
        

        return JsonResponse({'status_code': 1, 'new_survey_id': new_survey.survey_id})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


@csrf_exempt
def save_entire_survey(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        req = json.loads(request.body)
        # print(req)
        survey_id = req['qn_id']
        try:
            survey = Survey.objects.get(survey_id=survey_id)
        except:
            return JsonResponse({'status_code': 2, 'message': r'survey not exists'})
        save_survey_util(req, survey_id)
        # if survey.question_num == 0:
        #     return JsonResponse({'status_code': 3, 'message': r'no question'})
        return JsonResponse({'status_code': 1})
    else:
        return JsonResponse({'status_code': 4, 'message': r'method error'})


# util function

def save_survey_util(req, survey_id):
    survey = Survey.objects.get(survey_id=survey_id)
    title = req['title']
    description = req['description']
    questions = Question.objects.filter(survey_id=survey_id)

    try:
        survey.max_submission = req['max_recycling']
    except:
        pass

    try:
        survey.duration = req['duration']
    except:
        pass

    # if title == '':
    #     survey.survey_title = "新建问卷"
    # else:
    #     survey.survey_title = title

    if title:
        survey.survey_title = title

    # if description == '':
    #     if type == '1':
    #         description = "默认简介 1"
    #     elif type == '2':
    #         description = "默认简介 2"
    #     elif type == '3':
    #         description = "默认简介 3"
    #     else:
    #         description = "默认简介 4"
    # else:
    #     survey.survey_description = description

    if description:
        survey.survey_description = description
    
    # survey.survey_type = req['type']
    print("survey type: " + survey.survey_type)
    if req['finished_time']:
        survey.deadline = req['finished_time']
    
    try:
        survey.is_random = req['is_random']
    except:
        pass

    #save questions
    question_list = req['questions']

    survey.question_num = 0
    for question in question_list:
        print("enter count")
        survey.question_num += 1
    
    for question in questions:
        flag = 0
        for front_question in list(question_list):
            if question.question_id == front_question['question_id']:
                flag = 1
                print(front_question)
                question.question_title = front_question['title']
                question.question_description = front_question['description']
                question.question_type = front_question['type']
                question.is_necessary = front_question['must']
                question.sequence_id = front_question['id']
                question.option_num = 0
                if survey.survey_type == '3':
                    print("enter here...")
                    question.score = front_question['point']
                    question.correct_answer = front_question['refer']
                if question.question_type == 'mark':
                    question.max_point = front_question['score']
                # print('question ans: ' + question.correct_answer)
                image_url = ''
                try:
                    imgList = front_question['imgList']
                    for img in imgList:
                        image_url += img['url'] + "-<^-^>-"
                except:
                    pass
                question.image_url = image_url
                question.save()
                print("save happens A")
                if question.question_type == 'radio' or question.question_type == 'checkbox':
                    options = front_question['options']
                    remove_options = Option.objects.filter(question_id=question.question_id)
                    for option in remove_options:
                        option.delete()
                    for front_option in options:
                        new_option = Option()
                        new_option.option_description = front_option['title']
                        new_option.sequence_id = front_option['id']
                        new_option.question_id = question
                        new_option.save()
                        question.option_num += 1
                question_list.remove(front_question)
                
        if flag == 0:
            question.delete()

    print(question_list)
    
    for front_question in list(question_list):
        print("success 9")
        question = Question()
        question.question_title = front_question['title']
        question.question_description = front_question['description']
        question.question_type = front_question['type']
        question.is_necessary = front_question['must']
        question.sequence_id = front_question['id']
        question.survey_id = survey
        print("success 10")
        print(front_question['id'])
        if survey.survey_type == '3':
            print("enter here...")
            question.score = front_question['point']
            question.correct_answer = front_question['refer']
        if question.question_type == 'mark':
            question.max_point = front_question['score']
        options = front_question['options']
        remove_options = Option.objects.filter(question_id=question.question_id)
        image_url = ''
        try:
            imgList = front_question['imgList']
            for img in imgList:
                image_url += img['url'] + "-<^-^>-"
        except:
            pass
        question.image_url = image_url
        question.save()
        print("save happens B")
        for option in remove_options:
            option.delete()
        for front_option in options:
            new_option = Option()
            new_option.option_description = front_option['title']
            new_option.sequence_id = front_option['id']
            new_option.question_id = question
            new_option.save()
            question.option_num += 1
        question_list.remove(front_question)
        
    survey.last_modified_time = make_aware(datetime.datetime.now())
    survey.save()
    return 1
    

    
    




