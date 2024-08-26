from django import forms

class create_option_form(forms.Form):
    description = forms.CharField(max_length=250)
    question_id = forms.IntegerField()
    sequence_id = forms.IntegerField()