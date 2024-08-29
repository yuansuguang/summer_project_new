from django import forms

class create_survey_form(forms.Form):
    # username = forms.CharField(max_length=30)
    title = forms.CharField(max_length=100,required=False)
    description = forms.CharField(max_length=250,required=False)
    type = forms.CharField(max_length=30)

class get_survey_id_form(forms.Form):
    survey_id = forms.IntegerField()

class update_survey_deadline_form(forms.Form):
    survey_id = forms.IntegerField()
    new_deadline = forms.CharField(max_length=32)  # 字符串格式，例如 '2024-01-01 12:00'

class update_survey_duration_form(forms.Form):
    survey_id = forms.IntegerField()
    new_duration = forms.IntegerField()  # 单位：分钟

class update_survey_max_submission_form(forms.Form):
    survey_id = forms.IntegerField()
    new_max_submission = forms.IntegerField()