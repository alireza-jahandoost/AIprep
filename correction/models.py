from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _
from jsonfield import JSONField

# Create your models here.

class QuestionType(models.Model):
    name = models.CharField(max_length=100)


class QuestionTypeData(models.Model):
    TYPE_TPO = 1
    TYPE_NEO = 2
    TYPE_CHOICES = [
        (TYPE_TPO, _("TPO")),
        (TYPE_NEO, _("NEO")),
    ]

    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    type_name = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, null=True, blank=True)
    type_number = models.PositiveIntegerField(null=True, blank=True)
    data = JSONField()


class Correction(models.Model):
    STATUS_CHOICES = [
        (0, _("Pending")),
        (1, _("Invalid")),
        (2, _("Corrected")),
    ]
    question_type_data = models.ForeignKey(QuestionTypeData, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField(blank=True, null=True)
    correction = models.TextField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
