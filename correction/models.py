from authentication.models import CustomUser as User
from django.db import models
from django.utils.translation import gettext as _
from jsonfield import JSONField

# Create your models here.

class QuestionTypeData(models.Model):
    EXAM_DB_TPO = 1
    EXAM_DB_NEO = 2
    EXAM_DB_CHOICES = [
        (EXAM_DB_TPO, _("TPO")),
        (EXAM_DB_NEO, _("NEO")),
    ]

    EXAM_TYPE_TOEFL_TASK1 = 1
    EXAM_TYPE_TOEFL_TASK2 = 2
    EXAM_TYPE_CHOICES = [
        (EXAM_TYPE_TOEFL_TASK1, 'Toefl task1'),
        (EXAM_TYPE_TOEFL_TASK2, 'Toefl task2'),
    ]

    exam_type = models.PositiveSmallIntegerField(choices=EXAM_TYPE_CHOICES)
    exam_db_name = models.PositiveSmallIntegerField(choices=EXAM_DB_CHOICES)
    exam_db_number = models.PositiveIntegerField()
    data = JSONField()


class Correction(models.Model):
    STATUS_PENDING = 0
    STATUS_INVALID = 1
    STATUS_CORRECTED = 2
    STATUS_CHOICES = [
        (STATUS_PENDING, _("Pending")),
        (STATUS_INVALID, _("Invalid")),
        (STATUS_CORRECTED, _("Corrected")),
    ]
    question_type_data = models.ForeignKey(QuestionTypeData, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField(blank=True, null=True)
    correction = models.TextField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
