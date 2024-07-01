import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from correction.models import Correction, QuestionTypeData


def validate_min_number_of_words(min_number_of_words, name_of_field):
    def validator(value):
        words = re.findall("[a-zA-Z_]+", value)
        if len(words) < min_number_of_words:
            raise ValidationError(
                _("%(name_of_field)s does not contain at least %(min_number_of_words)s words."),
                params={"name_of_field": name_of_field, "min_number_of_words": min_number_of_words}
            )
    return validator


class ToeflIntegratedForm(forms.Form):
    question_type_name = forms.ChoiceField(choices=QuestionTypeData.TYPE_CHOICES)
    question_type_number = forms.CharField()
    answer = forms.CharField(widget=forms.Textarea(), validators=[validate_min_number_of_words(150, "answer")])


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg