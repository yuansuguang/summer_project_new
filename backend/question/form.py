from django import forms

class create_question_form(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=250)
    type = forms.CharField(max_length=30)
    survey_id = forms.IntegerField()
    sequence_id = forms.IntegerField()

class change_question_sequence_form(forms.Form):
    question_id = forms.IntegerField()
    cur_sequence_id = forms.IntegerField()


class list_question_form(forms.Form):
    survey_id = forms.IntegerField()



class list_question_forfill_form(forms.Form):
    code = forms.CharField(max_length=1024)

class list_question_forpreview_form(forms.Form):
    survey_id = forms.IntegerField()