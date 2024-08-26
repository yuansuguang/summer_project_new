from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import Option
from survey.models import *
from utils import hashcode
from django.views.decorators.csrf import csrf_exempt
from option.form import *

# 修改选择题属性描述option_description
@csrf_exempt
def change_option_description(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    if request.method == 'POST':
        option_id = request.POST.get('option_id')
        new_description = request.POST.get('new_description')

        if not all([option_id, new_description]):
            return JsonResponse({'status_code': 2, 'message': r'Missing required parameters.'})

        try:
            option = Option.objects.get(option_id=option_id)
        except:
            return JsonResponse({'status_code': 3, 'message': r'Option does not exist.'})

        option.option_description = new_description
        option.save()

        return JsonResponse({'status_code': 1, 'option_id': option_id})
    else:
        return JsonResponse({'status_code': 4, 'message': r'Method not allowed.'})


# 修改选择题属性排序数sequence_id
@csrf_exempt
def change_option_sequence_id(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    if request.method == 'POST':
        option_id = request.POST.get('option_id')
        new_sequence_id = request.POST.get('new_sequence_id')

        if not all([option_id, new_sequence_id]):
            return JsonResponse({'status_code': 2, 'message': r'Missing required parameters.'})

        try:
            option = Option.objects.get(id=option_id)
        except:
            return JsonResponse({'status_code': 3, 'message': r'Option does not exist.'})

        try:
            new_sequence_id = int(new_sequence_id)
        except ValueError:
            return JsonResponse({'status_code': 4, 'message': r'Invalid sequence ID.'})

        question_id = option.question_id
        question = Question.objects.get(question_id=question_id)  
        options = Option.objects.filter(question=question).order_by('sequence_id')

        current_sequence_id = option.sequence_id
        if new_sequence_id > current_sequence_id:
            for opt in options:
                if opt.sequence_id > current_sequence_id and opt.sequence_id <= new_sequence_id:
                    opt.sequence_id -= 1
                    opt.save()
        else:
            for opt in options:
                if opt.sequence_id < current_sequence_id and opt.sequence_id >= new_sequence_id:
                    opt.sequence_id += 1
                    opt.save()

        option.sequence_id = new_sequence_id
        option.save()

        return JsonResponse({'status_code': 1, 'new_sequence_id': new_sequence_id})
    else:
        return JsonResponse({'status_code': 5, 'message': r'Method not allowed.'})


@csrf_exempt
def option_create(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    if request.method == 'POST':
        option_form = create_option_form(request.POST)
        if option_form.is_valid():
            new_option = Option()
            description = option_form.cleaned_data.get('description')
            question_id = option_form.cleaned_data.get('question_id')
            sequence_id = option_form.cleaned_data.get('sequence_id')

            try:
                question = Question.objects.get(question_id=question_id)
            except:
                return JsonResponse({'status_code': 2, 'message': r'question not exists'})
            
            if question.question_type != '1' and question.question_type != '2':
                return JsonResponse({'status_code': 3, 'message': r'Question type error'})

            if description == '':
                description = "默认选项"
            
            new_option.option_description = description
            new_option.question_id = question_id
            new_option.sequence_id = sequence_id

            new_option.save()

            question.option_num += 1

            question.save()

            return JsonResponse({'status_code': 1, 'new_option_id': new_option.option_id})
        
        else:
            return JsonResponse({'status_code': 4, 'message': r'form error'})
    else:
        return JsonResponse({'status_code': 5, 'message': r'Method error'})


@csrf_exempt
def option_delete(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    if request.method == 'POST':
        option_id = request.POST.get('option_id')
        try:
            cur_option = Option.objects.get(option_id=option_id)
        except:
            return JsonResponse({'status_code': 2, 'message': r'option not exists'})
        
        cur_question_id = cur_option.question_id
        cur_sequence_id = cur_option.sequence_id
        options = Option.objects.filter(question_id=cur_question_id)
        for option in options:
            if option.sequence_id > cur_sequence_id:
                option.sequence_id = option.sequence_id - 1
                option.save()
        cur_option.delete()

        question = Question.objects.get(question_id=cur_question_id)
        question.option_num -= 1

        return JsonResponse({'status_code': 1})
    else:
        return JsonResponse({'status_code': 3, 'message': r'Method error'})