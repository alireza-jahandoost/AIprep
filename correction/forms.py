from django import forms

from correction.models import Correction, QuestionTypeData


class ToeflIntegratedForm(forms.Form):
    question_type_name = forms.ChoiceField(choices=QuestionTypeData.TYPE_CHOICES)
    question_type_number = forms.CharField()
    answer = forms.CharField(widget=forms.Textarea())


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg
