from django.db import models

class Survey(models.Model):
    survey_id = models.AutoField(primary_key=True)
    survey_title = models.CharField(max_length=100)
    survey_description = models.CharField(max_length=250, null=True, blank=True)
    username = models.CharField(max_length=30)

    # time-related properties
    create_time = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified_time = models.DateTimeField(editable=True)
    deadline = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True) # 考试问卷的时长，以 min 为单位

    # submission properties
    submission_num = models.IntegerField(default=0)
    max_submission = models.IntegerField(default=99999)

    # status properties
    is_available = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_collected = models.BooleanField(default=False)

    # question properties
    question_num = models.IntegerField(default=0)
    max_question_num = models.IntegerField(default=99999)

    # share
    share_code = models.CharField(max_length=1024, null=True)

    # question random
    is_random = models.BooleanField(default=False)

    SURVEY_TYPE_CHOICES = [
        (1, '普通问卷'),
        (2, '投票问卷'),
        (3, '考试问卷'),
        (4, '报名问卷')
    ]

    survey_type = models.CharField(max_length=30, default='')

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_title = models.CharField(max_length=100)
    question_description = models.CharField(max_length=250, null=True, blank=True)
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)

    # basic properties
    is_necessary = models.BooleanField(default=False)
    sequence_id = models.IntegerField(default=0) # 题目在问卷里是第几题

    # 问题是否隐藏，比如问题 A 回答了是就要同时回答问题 B，回答否就不答问题 B
    is_hidden = models.BooleanField(default=False)

    # QUESTION_TYPE_CHOICES = [
    #     (1, '单选题'),
    #     (2, '多选题'),
    #     (3, '填空题'),
    #     (4, '评分题')
    # ]

    # 发生了一些变化，为了和前端匹配，radio=单选，checkbox=多选，text=填空，mark=评分

    question_type = models.CharField(max_length=30, default='')

    # choices
    option_num = models.IntegerField(default=0)
    max_option_num = models.IntegerField(default=99999)

    # exam
    score = models.IntegerField(default=0)
    correct_answer = models.CharField(max_length=250)

    # vote
    max_point = models.IntegerField(default=0)
    
    # image
    image_url = models.CharField(max_length=255, null=True, blank=True)


class Option(models.Model):
    option_id = models.AutoField(primary_key=True)
    option_description = models.CharField(max_length=250, null=True, blank=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    sequence_id = models.IntegerField(default=0)


class Survey_submit(models.Model):
    survey_submit_id = models.AutoField(primary_key=True)
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    survey_submit_time = models.DateTimeField(auto_now_add=True)

    #properties
    is_submitted = models.BooleanField(default=False)
    survey_score = models.IntegerField(default=0)

    username = models.CharField(max_length=30)


class Question_submit(models.Model):
    question_submit_id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    survey_submit_id = models.ForeignKey(Survey_submit, on_delete=models.CASCADE)
    answer = models.CharField(max_length=250)
    username = models.CharField(max_length=30)
    score = models.IntegerField(default=0, null=True)

    # QUESTION_TYPE_CHOICES = [
    #     (1, '单选题'),
    #     (2, '多选题'),
    #     (3, '填空题'),
    #     (4, '评分题')
    # ]

    question_type = models.CharField(max_length=20, default='')






# Create your models here.
