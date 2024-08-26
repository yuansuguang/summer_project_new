from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from survey.models import *
from image.models import *
from image.form import *
from survey_planet.settings import *

import os
import uuid


@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        imageForm = upload_image_form(request.POST, request.FILES)
        if imageForm.is_valid():
            image = imageForm.cleaned_data.get('image')
            if image.name.split('.')[-1] not in ['jpeg', 'jpg', 'png']:
                return JsonResponse({'status_code': 2, 'message': r'image format error'})
            
            imageinstance = ImageFile(instance=image)
            imageinstance.save()

            imagename = imageinstance.instance.name.split('/')[-1]
            imageurl = WEB_ROOT + imageinstance.instance.url
            return JsonResponse({'status_code': 1, 'name': imagename, 'url': imageurl})
        else:
            return JsonResponse({'status_code': 3, 'message': r'invalid form'})
    else:
        return JsonResponse({'status_code': 4, 'message': r'invalid method'})



# @csrf_exempt
# def upload_image(request):

#     if request.method == 'POST':
#         # 获取上传的图片文件
#         image_file = request.FILES.get('image')
#         question_id = request.POST.get('question_id')

#         if image_file and question_id:
#             try:
#                 question = Question.objects.get(question_id=question_id)
#             except Question.DoesNotExist:
#                 return JsonResponse({'success': False, 'message': 'Question not found'})

#             # 检查图片格式
#             allowed_formats = ['jpg', 'jpeg', 'png']
#             file_extension = image_file.name.split('.')[-1].lower()
#             if file_extension not in allowed_formats:
#                 return JsonResponse({'success': False, 'message': 'Invalid image format'})

#             # 检查图片大小
#             max_size = 5 * 1024 * 1024  # 5MB
#             if image_file.size > max_size:
#                 return JsonResponse({'success': False, 'message': 'Image size too large'})

#             # 使用 uuid 生成唯一的文件名
#             new_file_name = f'{uuid.uuid4()}.{file_extension}'

#             # 构造图片保存路径
#             image_dir = os.path.join(settings.MEDIA_ROOT, 'survey_images')
#             if not os.path.exists(image_dir):
#                 os.makedirs(image_dir)
#             image_path = os.path.join(image_dir, new_file_name)

#             # 保存图片到指定路径
#             with open(image_path, 'wb') as f:
#                 for chunk in image_file.chunks():
#                     f.write(chunk)

#             # 保存图片 URL 到 Question 模型
#             question.image_url = f'{settings.MEDIA_URL}survey_images/{new_file_name}'
#             question.save()

#             return JsonResponse({'success': True, 'image_url': question.image_url})
#         else:
#             return JsonResponse({'success': False, 'message': 'No image selected or question_id not provided'})
#     else:
#         return JsonResponse({'success': False, 'message': 'Incorrect request method'})


@csrf_exempt
def delete_image(request):

    if request.method == 'POST':
        question_id = request.POST.get('question_id')

        if question_id:
            try:
                question = Question.objects.get(question_id=question_id)
            except Question.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Question not found'})

            # 删除图片文件
            if question.image_url:
                image_path = os.path.join(settings.MEDIA_ROOT, question.image_url.split(settings.MEDIA_URL)[-1])
                try:
                    os.remove(image_path)
                except Exception as e:
                    return JsonResponse({'success': False, 'message': f'Failed to delete image: {str(e)}'})

            # 清空图片 URL
            question.image_url = ''
            question.save()

            return JsonResponse({'success': True, 'message': 'Image deleted'})
        else:
            return JsonResponse({'success': False, 'message': 'question_id not provided'})
    else:
        return JsonResponse({'success': False, 'message': 'Incorrect request method'})
