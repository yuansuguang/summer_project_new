from django import forms

class clear_survey_submit_form(forms.Form):
    survey_id = forms.IntegerField()

class clear_single_submit_form(forms.Form):
    submit_id = forms.IntegerField()