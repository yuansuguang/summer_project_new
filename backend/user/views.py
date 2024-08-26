from django.shortcuts import render
from django.http import JsonResponse
# from captcha.models import CaptchaStore
# from captcha.helpers import captcha_image_url
from user.models import *
from user.sender import *
from .form import *
from django.contrib.auth.hashers import make_password, check_password
from utils import hashcode
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

import re
import json

# Create your views here.

@csrf_exempt
def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')

            print("success point 1")

            if User.objects.filter(username=username).exists():
                return JsonResponse({'status_code': 2, 'message': r'repeating username'})
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'status_code': 3, 'message': r'repeating email'})
            
            if password1 != password2:
                return JsonResponse({'status_code': 4, 'message': r'not same password'})
            
            new_user = User()
            new_user.username = username
            print("success point 2")
            new_user.password = make_password(password1)
            # print(new_user.password)
            print("success point 3")
            new_user.email = email
            new_user.save()
            print("success point 4")

            code = make_code(new_user)

            if send_code_email(email, code) == False:
                new_user.delete()
                return JsonResponse({'status code': 5, 'message': r'send mail failure'})

            return JsonResponse({'status_code': 1})
        
        else:
            print(register_form.errors)
            return JsonResponse({'status_code': -1})
    else:
        return render(request, 'test.html')


def user_confirm(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        try:
            confirm_code = ConfirmCode.objects.get(code=code)
        except:
            return render(request, 'incorrect.html')
        
        user = confirm_code.user
        user.user_confirm = True
        user.save()
        confirm_code.delete()
        return render(request, 'correct.html')


@csrf_exempt
# @api_view['POST']
def login(request):
    # if request.session.get('is_login'):
        # return JsonResponse({'status_code': 2, 'message': r'already logged in'})
    
    login_form = LoginForm(request.POST)

    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')

        print(username)
        print(password)

        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({'status_code': 3, 'message': r'username not found'})
    
        if check_password(password, user.password):
            request.session['is_login'] = True
            request.session['username'] = username

            print(username + ": log in") # debug test

            if user.user_confirm == False:
                return JsonResponse({'status_code': 4, 'message': r'unverified account'})        
            return JsonResponse({'status_code': 1})
        else:
            return JsonResponse({'status_code': 5, 'message': r'wrong password'})
    else:
        return JsonResponse({'status_code': -1})

@csrf_exempt
def logout(request):
    if not request.session.get('is_login', None):
        return JsonResponse({'status_code': 401})
    
    request.session.flush()

    return JsonResponse({'status_code': 200})

@csrf_exempt
def get_user_info(request):
    if not request.session.get('is_login', None):
        return JsonResponse({'status_code': 2, 'message': r'not logged in'})
    
    username = request.session.get('username')
    print(username + ": enter userinfo") # debug test

    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({'status_code': 3, 'message': r'username not found'})
    
    print("enter userinfo success") # debug test

    return JsonResponse({'status_code': 1, 'username': user.username, 'email': user.email})

        
@csrf_exempt
def change_password(request):
    if not request.session.get('is_login', None):
        return JsonResponse({'status_code': 2, 'message': r'not logged in'})

    if request.method == 'POST':
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            username = request.session.get('username')
            old_password = change_password_form.cleaned_data.get('old_password')
            new_password1 = change_password_form.cleaned_data.get('new_password1')
            new_password2 = change_password_form.cleaned_data.get('new_password2')
            try:
                user = User.objects.get(username=username)
            except:
                return JsonResponse({'status_code': 3, 'message': r'username not found'})

            if not check_password(old_password, user.password):
                return JsonResponse({'status_code': 4, 'message': r'wrong old password'})

            if new_password1 != new_password2:
                return JsonResponse({'status_code': 5, 'message': r'not same new password'})

            user.password = make_password(new_password1)
            user.save()

            return JsonResponse({'status_code': 1, 'message': r'password changed successfully'})
        else:
            return JsonResponse({'status_code': 6, 'message': r'invalid form data'})
    else:
        return JsonResponse({'status_code': 7, 'message': r'method not allowed'}) 
    

#重置密码    
@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'status_code': 2, 'message': r'email not found'})

            code = make_code(user)  # 生成重置密码链接
            ConfirmCode.objects.create(user=user, code=code)
            if send_reset_password_email(email, code) == False:  
                return JsonResponse({'status_code': 3, 'message': r'Failed to send mail'})

            return JsonResponse({'status_code': 1, 'message': r'success'})
        else:
            return JsonResponse({'status_code': 4, 'message': r'form.errors'})
    else:
        return JsonResponse({'status_code': 5, 'message': r'method not allowed'})
    
@csrf_exempt
def reset_password_confirm(request, code):
    if request.method == 'POST':   #部分验证，可以与code = request.GET.get('code')对比，选择其中一种 
        try:
            confirm_code = ConfirmCode.objects.get(code=code)
        except ConfirmCode.DoesNotExist:
            return JsonResponse({'status_code': 2, 'message': r'not valid'})

        form = SetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('new_password1')
            confirm_code.user.password = make_password(password)
            confirm_code.user.save()
            confirm_code.delete()
            return JsonResponse({'status_code': 1, 'message': r'success'})
        else:
            return JsonResponse({'status_code': 3, 'message': r'form.errors'})
    else:
        return JsonResponse({'status_code': 4, 'message': r'method not allowed'})
    
       