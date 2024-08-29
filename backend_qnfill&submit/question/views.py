from django.shortcuts import render
from django.http import JsonResponse
# from captcha.models import CaptchaStore
# from captcha.helpers import captcha_image_url
from survey.models import *
from utils import hashcode
from django.views.decorators.csrf import csrf_exempt
from question.form import *
from django.utils import timezone

import json
import datetime

# Create your views here.


@csrf_exempt
def list_question(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        listform = list_question_form(request.POST)
        if listform.is_valid():
            survey_id = listform.cleaned_data.get('survey_id')
            survey = Survey.objects.get(survey_id=survey_id)
            questions = Question.objects.filter(survey_id=survey_id).order_by('sequence_id')
            response = []

            for question in questions:
                options = Option.objects.filter(question_id=question.question_id)
                jsonoptions = []
                for option in options:
                    item = {"hasNumLimit": False,
                            "title": option.option_description,
                            "id": option.sequence_id,
                            "supply": 1,
                            "consume": 0}
                    jsonoptions.append(item)
                # if question.image_url != '':
                #     imgurllist = question.image_url.split("-<^-^>-")
                item = {"question_id": question.question_id,
                        "type": question.question_type,
                        "title": question.question_title,
                        "description": question.question_description,
                        "must": question.is_necessary,
                        "is_shown": question.is_hidden,
                        "id": question.sequence_id,
                        "question_type": question.question_type,
                        "option_num": question.option_num,
                        "point": question.score,
                        "row": 1,
                        "imgList": [],
                        "videoList": [],
                        "refer": question.correct_answer,
                        "score": question.max_point,
                        "options": jsonoptions}
                if question.image_url != '':
                    imgurllist = question.image_url.split("-<^-^>-")
                    for img in imgurllist:
                        item['imgList'].append({
                            'url': img,
                            'name': img.split('/')[-1]
                        })
                    del(item['imgList'][-1])
                response.append(item)

            return JsonResponse({'status_code': 1, 'data': json.dumps(response, ensure_ascii=False), 'title': survey.survey_title, 'description': survey.survey_description})
        else:
            return JsonResponse({'status_code': 2, 'message': r'form not valid'})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})
    




@csrf_exempt
def list_question_foranalysis(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        listform = list_question_form(request.POST)
        if listform.is_valid():
            survey_id = listform.cleaned_data.get('survey_id')
            questions1 = Question.objects.filter(survey_id=survey_id, question_type='radio')
            questions2 = Question.objects.filter(survey_id=survey_id, question_type='checkbox')
            questions = questions1.union(questions2)
            response = []

            for question in questions:
                options = Option.objects.filter(question_id=question.question_id)
                jsonoptions = []
                for option in options:
                    item = {"hasNumLimit": False,
                            "title": option.option_description,
                            "id": option.sequence_id,
                            "supply": 1,
                            "consume": 0}
                    jsonoptions.append(item)
                item = {"question_id": question.question_id,
                        "type": question.question_type,
                        "title": question.question_title,
                        "description": question.question_description,
                        "must": question.is_necessary,
                        "is_shown": question.is_hidden,
                        "id": question.sequence_id,
                        "question_type": question.question_type,
                        "option_num": question.option_num,
                        "point": question.score,
                        "row": 1,
                        "imgList": [],
                        "videoList": [],
                        "refer": question.correct_answer,
                        "score": question.max_point,
                        "options": jsonoptions}
                # if question.image_url != '':
                #     imgurllist = question.image_url.split("-<^-^>-")
                #     for img in imgurllist:
                #         item['imgList'].append({
                #             'url': img,
                #             'name': img.split('/')[-1]
                #         })
                #     del(item['imgList'][-1])
                response.append(item)

            return JsonResponse({'status_code': 1, 'data': json.dumps(response, ensure_ascii=False)})
        else:
            return JsonResponse({'status_code': 2, 'message': r'form not valid'})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


@csrf_exempt
def list_question_alt(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        listform = list_question_forfill_form(request.POST)
        if listform.is_valid():
            code = listform.cleaned_data.get('code')
            print(code)
            survey = Survey.objects.get(share_code=code)
            print(survey.survey_title)
            
            if survey.is_available == False:
                return JsonResponse({'status_code': 4, 'message': r'survey not available'})
            if survey.is_random:
                questions = Question.objects.filter(survey_id=survey).order_by('?')
            else:
                questions = Question.objects.filter(survey_id=survey).order_by('sequence_id')

            response = []

            for question in questions:
                options = Option.objects.filter(question_id=question.question_id)
                jsonoptions = []
                for option in options:
                    item = {"hasNumLimit": False,
                            "title": option.option_description,
                            "id": option.sequence_id,
                            "supply": 1,
                            "consume": 0}
                    jsonoptions.append(item)
                # if question.image_url != '':
                #     imgurllist = question.image_url.split("-<^-^>-")
                item = {"question_id": question.question_id,
                        "type": question.question_type,
                        "title": question.question_title,
                        "description": question.question_description,
                        "must": question.is_necessary,
                        "is_shown": question.is_hidden,
                        "id": question.sequence_id,
                        "question_type": question.question_type,
                        "option_num": question.option_num,
                        "point": question.score,
                        "row": 1,
                        "imgList": [],
                        "videoList": [],
                        "refer": question.correct_answer,
                        "score": question.max_point,
                        "options": jsonoptions}
                if question.image_url != '':
                    imgurllist = question.image_url.split("-<^-^>-")
                    for img in imgurllist:
                        item['imgList'].append({
                            'url': img,
                            'name': img.split('/')[-1]
                        })
                    del(item['imgList'][-1])
                response.append(item)
                print("check alt 1")
            try:
                print("try begin")
                survey_submit = Survey_submit.objects.get(username=request.session.get('username'), survey_id=survey)
                print("find survey submit")
                questions_submit = Question_submit.objects.filter(survey_submit_id=survey_submit)
                print("find questions submit")
                print(questions_submit.count())
                qs_submit = []
                for qss_submit in questions_submit:
                    print("enter submissions")
                    cor_question = qss_submit.question_id
                    if cor_question.question_type == 'checkbox':
                        ans_list = qss_submit.answer.split("-<^-^>-")
                        item = {"question_id": cor_question.sequence_id,
                                "type": cor_question.question_type,
                                "ans": '',
                                "ansList": ans_list,
                                "answer": cor_question.correct_answer,
                                "score": qss_submit.score}
                    else:
                        print("enter here")
                        item = {"question_id": cor_question.sequence_id,
                                "type": cor_question.question_type,
                                "ans": qss_submit.answer,
                                "ansList": [],
                                "answer": cor_question.correct_answer}
                    qs_submit.append(item)
                return JsonResponse({'status_code': 1, 'surveyId': survey.survey_id, 'survey_type': survey.survey_type, 'resume': survey.max_submission - survey.submission_num, 'title': survey.survey_title, 'description': survey.survey_description, 'duration': survey.duration, 'data': json.dumps(response, ensure_ascii=False), 'has_answers': 1, 'answers': json.dumps(qs_submit, ensure_ascii=False)})
            except:
                return JsonResponse({'status_code': 1, 'surveyId': survey.survey_id, 'survey_type': survey.survey_type, 'resume': survey.max_submission - survey.submission_num, 'title': survey.survey_title, 'description': survey.survey_description, 'duration': survey.duration, 'data': json.dumps(response, ensure_ascii=False), 'has_answers': 0})
            
        else:
            return JsonResponse({'status_code': 2, 'message': r'error2'})
        # survey = Survey.objects.get(share_code=code)
        # questions = Question.objects.filter(survey_id=survey).order_by('sequence_id')
        # response = []

        # for question in questions:
        #     options = Option.objects.filter(question_id=question.question_id)
        #     jsonoptions = []
        #     for option in options:
        #         item = {"hasNumLimit": False,
        #                 "title": option.option_description,
        #                 "id": option.sequence_id,
        #                 "supply": 1,
        #                 "consume": 0}
        #         jsonoptions.append(item)
        #     # if question.image_url != '':
        #     #     imgurllist = question.image_url.split("-<^-^>-")
        #     item = {"question_id": question.question_id,
        #             "type": question.question_type,
        #             "title": question.question_title,
        #             "description": question.question_description,
        #             "must": question.is_necessary,
        #             "is_shown": question.is_hidden,
        #             "id": question.sequence_id,
        #             "question_type": question.question_type,
        #             "option_num": question.option_num,
        #             "point": question.score,
        #             "row": 1,
        #             "imgList": [],
        #             "videoList": [],
        #             "refer": question.correct_answer,
        #             "score": question.max_point,
        #             "options": jsonoptions}
        #     # if question.image_url != '':
        #     #     imgurllist = question.image_url.split("-<^-^>-")
        #     #     for img in imgurllist:
        #     #         item['imgList'].append({
        #     #             'url': img,
        #     #             'name': img.split('/')[-1]
        #     #         })
        #     #     del(item['imgList'][-1])
        #     response.append(item)

        # return JsonResponse({'status_code': 1, 'data': json.dumps(response, ensure_ascii=False)})
        
        # else:
        #     return JsonResponse({'status_code': 2, 'message': r'form not valid'})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


@csrf_exempt
def list_question_forfill(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        listform = list_question_forfill_form(request.POST)
        if listform.is_valid():
            code = listform.cleaned_data.get('code')
            print(code)
            survey = Survey.objects.get(share_code=code)
            print(survey.survey_title)
            questions = Question.objects.filter(survey_id=survey.survey_id).order_by('sequence_id')
            response = []

            for question in questions:
                options = Option.objects.filter(question_id=question.question_id)
                print(options)
                jsonoptions = []
                for option in options:
                    item = {"hasNumLimit": False,
                            "title": option.option_description,
                            "id": option.sequence_id,
                            "supply": 1,
                            "consume": 0}
                    jsonoptions.append(item)
                item = {"question_id": question.question_id,
                        "type": question.question_type,
                        "title": question.question_title,
                        "description": question.question_description,
                        "must": question.is_necessary,
                        "is_shown": question.is_hidden,
                        "id": question.sequence_id,
                        "question_type": question.question_type,
                        "option_num": question.option_num,
                        "point": question.score,
                        "row": 1,
                        "imgList": [],
                        "videoList": [],
                        "ref": question.correct_answer,
                        "options": jsonoptions}
                # if question.image_url != '':
                #     imgurllist = question.image_url.split("-<^-^>-")
                #     for img in imgurllist:
                #         item['imgList'].append({
                #             'url': img,
                #             'name': img.split('/')[-1]
                #         })
                #     del(item['imgList'][-1])
                response.append(item)
            print("test here")
            print(survey.duration)
            return JsonResponse({'status_code': 1, 'title': survey.survey_title, 'description': survey.survey_description, 'duration': survey.duration, 'data': json.dumps(response, ensure_ascii=False)})
        else:
            return JsonResponse({'status_code': 2, 'message': r'form not valid'})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})
    


@csrf_exempt
def list_question_forpreview(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        listform = list_question_forpreview_form(request.POST)
        if listform.is_valid():
            survey_id = listform.cleaned_data.get('survey_id')
            # print(code)
            survey = Survey.objects.get(survey_id=survey_id)
            print(survey.survey_title)
            questions = Question.objects.filter(survey_id=survey.survey_id).order_by('sequence_id')
            response = []

            for question in questions:
                options = Option.objects.filter(question_id=question.question_id)
                print(options)
                jsonoptions = []
                for option in options:
                    item = {"hasNumLimit": False,
                            "title": option.option_description,
                            "id": option.sequence_id,
                            "supply": 1,
                            "consume": 0}
                    jsonoptions.append(item)
                item = {"question_id": question.question_id,
                        "type": question.question_type,
                        "title": question.question_title,
                        "description": question.question_description,
                        "must": question.is_necessary,
                        "is_shown": question.is_hidden,
                        "id": question.sequence_id,
                        "question_type": question.question_type,
                        "option_num": question.option_num,
                        "point": question.score,
                        "row": 1,
                        "imgList": [],
                        "videoList": [],
                        "ref": question.correct_answer,
                        "options": jsonoptions}
                if question.image_url != '':
                    imgurllist = question.image_url.split("-<^-^>-")
                    for img in imgurllist:
                        item['imgList'].append({
                            'url': img,
                            'name': img.split('/')[-1]
                        })
                    del(item['imgList'][-1])
                response.append(item)

            return JsonResponse({'status_code': 1, 'title': survey.survey_title, 'description': survey.survey_description, 'data': json.dumps(response, ensure_ascii=False)})
        else:
            return JsonResponse({'status_code': 2, 'message': r'form not valid'})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


@csrf_exempt
def create_question(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        question_form = create_question_form(request.POST)
        if question_form.is_valid():
            new_question = Question()
            title = question_form.cleaned_data.get('title')
            description = question_form.cleaned_data.get('description')
            type = question_form.cleaned_data.get('type')
            survey_id = question_form.cleaned_data.get('survey_id')
            sequence_id = question_form.cleaned_data.get('sequence_id')

            if title == '':
                title = "新建问题"
            
            if description == '':
                if type == '1':
                    description = "默认简介 1"
                elif type == '2':
                    description = "默认简介 2"
                elif type == '3':
                    description = "默认简介 3"
                else:
                    description = "默认简介 4"
            
            new_question.question_title = title
            new_question.question_description = description
            new_question.question_type = type
            new_question.survey_id = survey_id
            new_question.sequence_id = sequence_id

            new_question.save()

            survey = Survey.objects.get(survey_id=survey_id)
            survey.question_num = survey.question_num + 1 

            survey.save()

            return JsonResponse({'status_code': 1, 'question_id': new_question.question_id})
        else:
            return JsonResponse({'status_code': 2, 'message': r'something went wrong with the form'})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


@csrf_exempt
def delete_question(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        try:
            cur_question = Question.objects.get(question_id=question_id)
        except:
            return JsonResponse({'status_code': 2, 'message': r'question not found'})
        
        cur_survey_id = cur_question.survey_id
        cur_sequence_id = cur_question.sequence_id
        questions = Question.objects.filter(survey_id=cur_survey_id)
        for question in questions:
            if question.sequence_id > cur_sequence_id:
                question.sequence_id = question.sequence_id - 1
                question.save()
        cur_question.delete()

        survey = Survey.objects.get(survey_id=cur_survey_id)
        survey.question_num = survey.question_num - 1 

        return JsonResponse({'status_code': 1})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


@csrf_exempt
def duplicate_question(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        try:
            cur_question = Question.objects.get(question_id=question_id)
        except:
            return JsonResponse({'status_code': 2, 'message': r'question not found'})
        new_question = Question()
        new_question.question_title=cur_question.question_title 
        new_question.question_description=cur_question.question_description,
        new_question.survey_id=cur_question.survey_id,
        new_question.is_necessray=cur_question.is_necessary,
        new_question.is_hidden=cur_question.is_hidden,
        new_question.question_type=cur_question.question_type,
        new_question.option_num=cur_question.option_num,
        new_question.score=cur_question.score,
        new_question.correct_answer=cur_question.correct_answer

        # maybe something to do with sequence_id

        if cur_question.question_type == '1' or cur_question.question_type == '2':
            cur_options = Option.objects.filter(question_id=cur_question.question_id)
            for option in cur_options:
                new_option = Option()
                new_option.option_description = option.option_description
                new_option.question_id = cur_question.question_id
                new_option.sequence_id = option.sequence_id
                new_option.save()
        new_question.save()

        cur_survey_id = new_question.survey_id
        survey = Survey.objects.get(survey_id=cur_survey_id)
        survey.question_num = survey.question_num + 1 

        return JsonResponse({'status_code': 1, 'new_question_id': new_question.question_id})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


@csrf_exempt
def change_question_sequence(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        sequence_form = change_question_sequence_form(request.POST)
        if sequence_form.is_valid():
            question_id = sequence_form.cleaned_data.get('question_id')
            cur_sequence_id = sequence_form.cleaned_data.get('cur_sequence_id')

            try:
                question = Question.objects.get(question_id=question_id)
            except:
                return JsonResponse({'status_code': 2, 'message': r'question not found'})

            pos = question.sequence_id
            survey_id = question.survey_id

            questions = Question.objects.filter(survey_id=survey_id)
            if cur_sequence_id > pos:
                for qs in questions:
                    if qs.sequence_id > pos and qs.sequence_id < cur_sequence_id:
                        qs.sequence_id = qs.sequence_id - 1
                        qs.save()
            else:
                for qs in questions:
                    if qs.sequence_id > cur_sequence_id and qs.sequence_id < pos:
                        qs.sequence_id = qs.sequence_id + 1
                        qs.save()

            question.sequence_id = cur_sequence_id
            question.save()

            return JsonResponse({'status_code': 1})
        else:
            return JsonResponse({'status_code': 3, 'message': r'something went wrong with the form'})
    else:
        return JsonResponse({'status_code': 4, 'message': r'method error'})
              
        
        
# 操作必答属性is_necessary        
@csrf_exempt
def change_question_is_necessary(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        try:
            cur_question = Question.objects.get(question_id=question_id)
        except:
            return JsonResponse({'status_code': 2, 'message': r'question not found'})
        
        cur_question.is_necessary = not cur_question.is_necessary
        cur_question.save()
        return JsonResponse({'status_code': 1})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


# 操作隐藏属性is_hidden       
@csrf_exempt
def change_question_is_hidden(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        try:
            cur_question = Question.objects.get(question_id=question_id)
        except:
            return JsonResponse({'status_code': 2, 'message': r'question not found'})
        
        cur_question.is_hidden = not cur_question.is_hidden
        cur_question.save()
        return JsonResponse({'status_code': 1})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})


# 操作问题分数属性score       
@csrf_exempt
def change_question_score(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})   

    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        score = request.POST.get('score')
        try:
            cur_question = Question.objects.get(question_id=question_id)
        except:
            return JsonResponse({'status_code': 2, 'message': r'question not found'})
        try:
            score = int(score)
            if score < 0:
                return JsonResponse({'status_code': 3, 'message': r'score must be a non-negative integer'})
        except:
            return JsonResponse({'status_code': 4, 'message': r'score must be an integer'})
        
        cur_question.score = score
        cur_question.save()
        return JsonResponse({'status_code': 1})
    else:
        return JsonResponse({'status_code': 5, 'message': r'method error'})
    
    
# 操作正确答案属性correct_answer
@csrf_exempt
def change_question_correct_answer(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        correct_answer = request.POST.get('correct_answer')
        try:
            cur_question = Question.objects.get(question_id=question_id)
        except:
            return JsonResponse({'status_code': 2, 'message': r'question not found'})

        # 可以根据需要添加对 correct_answer 格式的校验
        
        cur_question.correct_answer = correct_answer
        cur_question.save()
        return JsonResponse({'status_code': 1})
    else:
        return JsonResponse({'status_code': 3, 'message': r'method error'})

    