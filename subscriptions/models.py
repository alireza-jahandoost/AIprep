from authentication.models import CustomUser as User
from django.db import models


# Create your models here.
class Plan(models.Model):
    CORRECTION_TYPE_NORMAL = 0
    CORRECTION_TYPE_PRO = 1
    CORRECTION_TYPE_CHOICES = [
        (CORRECTION_TYPE_NORMAL, 'Normal'),
        (CORRECTION_TYPE_PRO, 'Pro'),
    ]

    plan_name = models.CharField(max_length=100)
    available_daily_corrections = models.IntegerField()
    correction_type = models.PositiveSmallIntegerField(choices=CORRECTION_TYPE_CHOICES)
    number_of_days = models.IntegerField()
    price = models.IntegerField()


class Payment(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_id = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    card_hash = models.CharField(max_length=100, null=True, blank=True)
    card_pan = models.CharField(max_length=100, null=True, blank=True)
    hide_payment = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)