from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
# from captcha.models import CaptchaStore
# from captcha.helpers import captcha_image_url
from survey.models import *
from utils import hashcode
from django.views.decorators.csrf import csrf_exempt
from question.form import *
from django.utils import timezone
from submit.form import *
from collections import Counter
from django.utils import timezone
from django.utils.timezone import make_aware


import json
import datetime

@csrf_exempt
def submit_survey(request):
    
    if request.method == 'POST':
        try:
            # 从请求体中解析 JSON 数据
            data = json.loads(request.body)
            code = data.get('code')  # 获取问卷 ID
            # username = data.get('username')  # 获取用户名
            try:
                username = request.session.get('username')
            except:
                username = "visitor"
            answers = data.get('answers')  # 获取答案列表

            print("checkpoint 0")


            # 判断提交的数据是否完整，可以前端判断，可删
            if not all([code, username, answers]):
                return JsonResponse({'status_code': 2, 'message': r'Incomplete data provided.'})

            # 获取问卷信息
            try:
                survey = Survey.objects.get(share_code=code)
            except Survey.DoesNotExist:
                return JsonResponse({'status_code': 3, 'message': r'Survey not found.'})

            # 检查是否达到最大提交次数
            if survey.submission_num >= survey.max_submission:
                return JsonResponse({'status_code': 4, 'message': r'Survey submission limit reached.'})
            
            # 检查问卷是否在可提交时间范围内
            now = timezone.now()
            if survey.deadline is not None and now > survey.deadline:
                return JsonResponse({'status_code': 5, 'message': r'Survey deadline exceeded.'})
            
            # 检查用户是否已经提交过该问卷
            if survey.survey_type != '1' and username != "visitor" and Survey_submit.objects.filter(survey_id=survey, username=username, is_submitted=True).exists():
                return JsonResponse({'status_code': 6, 'message': r'User has already submitted this survey.'})
            
            # # 获取用户 IP 地址
            # user_ip = get_client_ip(request)  # 最后定义 get_client_ip 函数

            # # 检查 IP 地址是否已经提交过该问卷  
            # if Survey_submit.objects.filter(survey_id=survey, user_ip=user_ip, is_submitted=True).exists():
            #     return JsonResponse({'status_code': 7, 'message': r'This IP address has already submitted this survey.'})
            
            # 创建新的问卷提交记录旧
            # survey_submit = Survey_submit.objects.create(
            #     survey_id=Survey.objects.get(survey_id=survey_id),  # 获取对应的问卷对象
            #     username=username
            # )
            
            # 创建新的问卷提交记录
            if username != "visitor":
                try:
                    survey_submit = Survey_submit.objects.get(survey_id=survey, username=username)
                except:
                    survey_submit = Survey_submit.objects.create(
                        survey_id=survey,
                        username=username,
                        survey_submit_time=make_aware(datetime.datetime.now())
                    )
            else:
                survey_submit = Survey_submit.objects.create(
                        survey_id=survey,
                        username=username,
                        survey_submit_time=make_aware(datetime.datetime.now())
                    )

            print("checkpoint 0.5")

            total_score = 0  # 初始化总分

            # 遍历每个答案
            for answer in answers:
                question_id = answer.get('question_id')  # 获取问题 ID
                answer_text = answer.get('answer')  # 获取答案内容

                # 判断答案数据是否完整，可以前端判断，可删
                # if not all([question_id, answer_text]):
                #     return JsonResponse({'status_code': 8, 'message': r'Incomplete answer data provided.'})

                # 获取对应的问题对象
                question = Question.objects.get(question_id=question_id)

                if answer_text == '' and question.is_necessary == True:
                    return JsonResponse({'status_code': 8, 'message': r'incomplete answer'})

                questionsub = Question_submit.objects.create(
                    question_id=question,
                    survey_submit_id=survey_submit,
                    answer=answer_text,
                    username=username,
                    question_type=question.question_type,
                )

                questionsub.save()

                # 如果是客观题并且有正确答案，则进行评分
                if question.correct_answer:  # 客观题有正确答案时
                    if answer_text == question.correct_answer:
                        total_score += question.score
                        questionsub.score = question.score
                        questionsub.save()

                # 创建问题提交记录
                
            
            print("checkpoint 1")

            # 更新问卷提交记录的总分和提交状态
            survey_submit.survey_score = total_score
            survey_submit.is_submitted = True
            survey_submit.save()
            #更新问卷提交次数
            survey.submission_num += 1
            survey.save()

            # 返回成功响应
            return JsonResponse({'status_code': 1, 'message': r'Survey submitted successfully.'})

        # 处理各种异常
        except json.JSONDecodeError:
            return JsonResponse({'status_code': 9, 'message': r'Invalid JSON data.'})  # JSON 数据解析错误
        except Survey.DoesNotExist:
            return JsonResponse({'status_code': 10, 'message': r'Survey not found.'})  # 未找到对应的问卷
        except Question.DoesNotExist:
            return JsonResponse({'status_code': 11, 'message': r'Question not found.'})  # 未找到对应的问题
        except Exception as e:
            print(str(e))
            return JsonResponse({'status_code': 12, 'message': f'An error occurred: {str(e)}'})  # 其他异常

    else:
        # 如果请求方法不是 POST，则返回错误响应
        return JsonResponse({'status_code': 13, 'message': r'Method not allowed.'})
    

@csrf_exempt
def save_survey(request):
    
    if request.method == 'POST':
        try:
            # 从请求体中解析 JSON 数据
            data = json.loads(request.body)
            code = data.get('code')  # 获取问卷 ID
            # username = data.get('username')  # 获取用户名
            username = request.session.get('username')
            answers = data.get('answers')  # 获取答案列表


            # 判断提交的数据是否完整，可以前端判断，可删
            if not all([code, username, answers]):
                return JsonResponse({'status_code': 2, 'message': r'Incomplete data provided.'})

            # 获取问卷信息
            try:
                survey = Survey.objects.get(share_code=code)
            except Survey.DoesNotExist:
                return JsonResponse({'status_code': 3, 'message': r'Survey not found.'})

            # # 检查是否达到最大提交次数
            # if survey.submission_num >= survey.max_submission:
            #     return JsonResponse({'status_code': 4, 'message': r'Survey submission limit reached.'})
            
            # 检查问卷是否在可提交时间范围内
            now = timezone.now()
            if survey.deadline is not None and now > survey.deadline:
                return JsonResponse({'status_code': 4, 'message': r'Survey deadline exceeded.'})
            
            # # 检查用户是否已经提交过该问卷
            # if Survey_submit.objects.filter(survey_id=survey, username=username, is_submitted=True).exists():
            #     return JsonResponse({'status_code': 6, 'message': r'User has already submitted this survey.'})
            
            # # 获取用户 IP 地址
            # user_ip = get_client_ip(request)  # 最后定义 get_client_ip 函数

            # # 检查 IP 地址是否已经提交过该问卷  
            # if Survey_submit.objects.filter(survey_id=survey, user_ip=user_ip, is_submitted=True).exists():
            #     return JsonResponse({'status_code': 7, 'message': r'This IP address has already submitted this survey.'})
            
            # 创建新的问卷提交记录旧
            # survey_submit = Survey_submit.objects.create(
            #     survey_id=Survey.objects.get(survey_id=survey_id),  # 获取对应的问卷对象
            #     username=username
            # )
            
            # 创建新的问卷提交记录
            try:
                survey_submit = Survey_submit.objects.get(survey_id=survey, username=username)
            except:
                survey_submit = Survey_submit.objects.create(
                    survey_id=survey,
                    username=username,
                    survey_submit_time=make_aware(datetime.datetime.now())
                )

            total_score = 0  # 初始化总分

            # 遍历每个答案
            for answer in answers:
                question_id = answer.get('question_id')  # 获取问题 ID
                answer_text = answer.get('answer')  # 获取答案内容

                # 判断答案数据是否完整，可以前端判断，可删
                # if not all([question_id, answer_text]):
                #     return JsonResponse({'status_code': 8, 'message': r'Incomplete answer data provided.'})

                # 获取对应的问题对象
                question = Question.objects.get(question_id=question_id)

                # 如果是客观题并且有正确答案，则进行评分
                if question.correct_answer:  # 客观题有正确答案时
                    if answer_text == question.correct_answer:
                        total_score += question.score

                # 创建问题提交记录
                try:
                    questionsub = Question_submit.objects.get(question_id=question)
                    questionsub.answer = answer_text
                    questionsub.save()
                except:
                    questionsub = Question_submit.objects.create(
                        question_id=question,
                        survey_submit_id=survey_submit,
                        answer=answer_text,
                        username=username,
                        question_type=question.question_type,
                    )
                    questionsub.save()

            # 更新问卷提交记录的总分和提交状态
            survey_submit.survey_score = total_score
            survey_submit.is_submitted = False #保存设为False
            survey_submit.save()
            # #更新问卷提交次数
            # survey.submission_num += 1
            # survey.save()

            # 返回成功响应
            return JsonResponse({'status_code': 1, 'message': r'Survey saved successfully.'})

        # 处理各种异常
        except json.JSONDecodeError:
            return JsonResponse({'status_code': 5, 'message': r'Invalid JSON data.'})  # JSON 数据解析错误
        except Survey.DoesNotExist:
            return JsonResponse({'status_code': 6, 'message': r'Survey not found.'})  # 未找到对应的问卷
        except Question.DoesNotExist:
            return JsonResponse({'status_code': 7, 'message': r'Question not found.'})  # 未找到对应的问题
        except Exception as e:
            return JsonResponse({'status_code': 8, 'message': f'An error occurred: {str(e)}'})  # 其他异常

    else:
        # 如果请求方法不是 POST，则返回错误响应
        return JsonResponse({'status_code': 9, 'message': r'Method not allowed.'})


#清空问卷
@csrf_exempt
def clear_survey(request):

    if request.method == 'POST':
        try:
            # 从请求体中解析 JSON 数据
            form = clear_survey_submit_form(request.POST)
            if form.is_valid():
                survey_id = form.cleaned_data.get('survey_id')
                # 获取问卷信息
                try:
                    survey = Survey.objects.get(survey_id=survey_id)
                except Survey.DoesNotExist:
                    return JsonResponse({'status_code': 2, 'message': r'Survey not found.'})

                # 删除该问卷的所有问题提交记录
                Question_submit.objects.filter(survey_submit_id__survey_id=survey).delete()
                #survey_submit_id__survey_id=survey: 筛选条件，使用了 Django ORM 的双下划线 __ 语法进行关联查询
                # 删除该问卷的所有问卷提交记录
                Survey_submit.objects.filter(survey_id=survey).delete()
                survey.submission_num = 0
                survey.save()
                return JsonResponse({'status_code': 1, 'message': r'Survey cleared successfully.'})
            else:
                return JsonResponse({'status_code': 3, 'message': r'Invalid form data.'}) 
        except Exception as e:
            return JsonResponse({'status_code': 4, 'message': f'An error occurred: {str(e)}'})
    else:
        return JsonResponse({'status_code': 5, 'message': r'Method not allowed.'})




@csrf_exempt
def get_submissions_by_question_id(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question_id = data.get('question_id')

            if not question_id:
                return JsonResponse({'status_code': 2, 'message': 'Question ID is required.'})

            # 只获取已提交问卷的结果
            submissions = Question_submit.objects.filter(
                question_id=question_id,
                survey_submit_id__is_submitted=True # 通过关联查询筛选已提交的问卷
            )

            # 将结果格式化为列表
            submission_list = []
            for submission in submissions:
                submission_data = {
                    'submission_id': submission.id,
                    #'username': submission.username,
                    'answer': submission.answer,
                    #'question_type': submission.question_type,
                }
                submission_list.append(submission_data)

            return JsonResponse({'status_code': 1, 'message': 'Submissions retrieved successfully.', 'submissions': submission_list})

        except json.JSONDecodeError:
            return JsonResponse({'status_code': 3, 'message': 'Invalid JSON data.'})
        except Exception as e:
            return JsonResponse({'status_code': 4, 'message': f'An error occurred: {str(e)}'})

    else:
        return JsonResponse({'status_code': 5, 'message': 'Method not allowed.'})
    
    
@csrf_exempt
def get_survey_submissions(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            survey_id = data.get('survey_id')
            print(survey_id)

            if not survey_id:
                return JsonResponse({'status_code': 2, 'message': 'Survey ID is required.'})

            try:
                survey = Survey.objects.get(survey_id=survey_id)
            except Survey.DoesNotExist:
                return JsonResponse({'status_code': 3, 'message': 'Survey not found.'})
            


            questions = Question.objects.filter(survey_id=survey_id)
            submissions_dict = {}  # 使用字典存储每个 submission_id 的答案

            for question in questions:
                question_submissions = Question_submit.objects.filter(
                    question_id=question.question_id,
                    survey_submit_id__is_submitted=True
                ).select_related('survey_submit_id')

                for qs in question_submissions:
                    submission_id = qs.survey_submit_id.survey_submit_id
                    if submission_id not in submissions_dict:
                        submissions_dict[submission_id] = []  # 初始化为空列表
                    submissions_dict[submission_id].append({
                        'question_description': question.question_description,
                        'answer': qs.answer
                    })

            submissions = list(submissions_dict.values())  # 转换为列表

            return JsonResponse({
                'status_code': 1,
                'message': 'Submissions retrieved successfully.',
                'submissions': submissions
            })

        except json.JSONDecodeError:
            return JsonResponse({'status_code': 4, 'message': 'Invalid JSON data.'})
        except Exception as e:
            print(str(e))
            return JsonResponse({'status_code': 5, 'message': str(e)})

    else:
        return JsonResponse({'status_code': 6, 'message': 'Method not allowed.'})


@csrf_exempt
def get_question_statistics(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question_id = data.get('question_id')

            if not question_id:
                return JsonResponse({'status_code': 2, 'message': 'Question ID is required.'})

            # 获取问题类型
            question = Question.objects.get(pk=question_id)
            question_type = question.question_type

            # 获取已提交问卷的答案
            answers = Question_submit.objects.filter(
                question_id=question_id,
                survey_submit_id__is_submitted=True
            ).values_list('answer', flat=True)

            if question_type in ('radio', 'checkbox'): # 单选题和多选题
                # 统计每个选项出现的次数
                option_counts = Counter()
                for answer in answers:
                    print(answer)
                    selected_options = answer.split('-<^-^>-')  # 多选题答案可能包含多个选项，用逗号分隔
                    print(selected_options)
                    option_counts.update(selected_options)
                
                print(option_counts)

                # 获取所有选项
                options = Option.objects.filter(question_id=question_id).values('option_id', 'option_description')

                # 将统计结果与选项描述合并
                statistics = []
                for option in options:
                    # option_id = str(option['option_id'])  # 转换为字符串，以便与 Counter 中的键匹配
                    option_description = option['option_description']
                    count = option_counts.get(option_description, 0) #待定 count = option_counts.get(option_id, 0)
                    statistics.append({
                        'name': option['option_description'],
                        'count': count
                    })
                print(statistics)

            elif question_type == 'mark':  # 评分题
                # 统计每个分数出现的次数
                score_counts = Counter(answers)

                # 将统计结果格式化为列表
                statistics = [{'score': score, 'count': count} for score, count in score_counts.items()]

            else:  # 其他类型题目，例如填空题，暂不进行统计
                statistics = []

            return JsonResponse({
                'status_code': 1,
                'message': 'Statistics retrieved successfully.',
                'statistics': statistics
            })

        except json.JSONDecodeError:
            return JsonResponse({'status_code': 3, 'message': 'Invalid JSON data.'})
        except Question.DoesNotExist:
            return JsonResponse({'status_code': 4, 'message': 'Question not found.'})
        except Exception as e:
            return JsonResponse({'status_code': 5, 'message': f'An error occurred: {str(e)}'})

    else:
        return JsonResponse({'status_code': 6, 'message': 'Method not allowed.'})

# #清空所有问卷
# @csrf_exempt
# def clear_all_survey(request):

#     if request.method == 'POST':
#         try:
#             # 删除所有问题提交记录
#             Question_submit.objects.all().delete()
#             # 删除所有问卷提交记录
#             Survey_submit.objects.all().delete()
#             return JsonResponse({'status_code': 1, 'message': r'Survey cleared successfully.'})
#         except Exception as e:
#             return JsonResponse({'status_code': 2, 'message': f'An error occurred: {str(e)}'})
#     else:
#         return JsonResponse({'status_code': 3, 'message': r'Method not allowed.'})

# #ip获取
# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip


@csrf_exempt
def get_user_submissions(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    
    if request.method == 'GET':
        username = request.session.get('username')
        try:
            submissions = Survey_submit.objects.filter(username=username)
        except:
            return JsonResponse({'status_code': 2, 'message': r'no survey'})

        response = []
        for submission in submissions:
            survey = submission.survey_id
            item = {'submitId': submission.survey_submit_id,
                    'creationDate': submission.survey_submit_time.strftime("%Y-%m-%d %H:%M"),
                    'questionnaireId': survey.survey_id,
                    'questionnaireName': survey.survey_title,
                    'code': survey.share_code,
                    'isSubmitted': submission.is_submitted,
                    'score': submission.survey_score,
                    'type': survey.survey_type}
            response.append(item)
        return JsonResponse({'status_code': 1, 'data': json.dumps(response, ensure_ascii=False)})
    
#删除特定提交
@csrf_exempt
def delete_submission(request):
    if request.method == 'POST':
        form = clear_single_submit_form(request.POST)
        if form.is_valid():
            submission_id = form.cleaned_data.get('submit_id')
            
            if not submission_id:
                return JsonResponse({'status_code': 2, 'message': 'Submission ID is required.'})

            try:
                # 获取提交记录
                submission = Survey_submit.objects.get(survey_submit_id=submission_id)
            except Survey_submit.DoesNotExist:
                return JsonResponse({'status_code': 3, 'message': 'Submission not found.'})

            # 删除关联的问题提交记录
            Question_submit.objects.filter(survey_submit_id=submission).delete()

            # 删除提交记录
            submission.delete()

            return JsonResponse({'status_code': 1, 'message': 'Submission deleted successfully.'})

        else:
            return JsonResponse({'status_code': 4, 'message': 'Invalid JSON data.'})
        

    else:
        return JsonResponse({'status_code': 6, 'message': 'Method not allowed.'})







