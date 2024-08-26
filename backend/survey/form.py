from django import forms

class list_survey_form(forms.Form):
    survey_keyword = forms.CharField(max_length=30, required=False)
    is_deleted = forms.BooleanField(required=False)
    is_collected = forms.BooleanField(required=False)
    is_released = forms.IntegerField(required=False)
    survey_type = forms.CharField(max_length=30, required=False)
    sort_key = forms.CharField(max_length=30, required=False)
    sort_type = forms.CharField(max_length=30, required=False)
    username = forms.CharField(max_length=30, required=False)


class share_survey_form(forms.Form):
    survey_id = forms.IntegerField()