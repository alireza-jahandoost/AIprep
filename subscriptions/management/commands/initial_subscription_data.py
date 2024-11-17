import os
import re
import string
import sys

from django.core.management import BaseCommand

from correction.models import QuestionTypeData
from subscriptions.models import Plan


class Command(BaseCommand):
    help = "Adds subscription plans to the database."

    def handle(self, *args, **options):
        # Normal Plan
        Plan.objects.create(plan_name="Normal",
                            available_daily_corrections=2,
                            correction_type=Plan.CORRECTION_TYPE_NORMAL,
                            number_of_days=-1,
                            price=0)

        # Pro Plan
        pro_prices = [147000, 347000, 497000]
        pro_days = [31, 91, 181]
        for i in range(len(pro_prices)):
            Plan.objects.create(plan_name='Pro',
                                available_daily_corrections=2,
                                correction_type=Plan.CORRECTION_TYPE_PRO,
                                number_of_days=pro_days[i],
                                price=pro_prices[i])

        # Pro Plus Plan
        pro_plus_prices = [197000, 447000, 597000]
        pro_plus_days = [31, 91, 181]
        for i in range(len(pro_prices)):
            Plan.objects.create(plan_name='Pro Plus',
                                available_daily_corrections=4,
                                correction_type=Plan.CORRECTION_TYPE_PRO,
                                number_of_days=pro_plus_days[i],
                                price=pro_plus_prices[i])

        # Trial plan
        Plan.objects.create(plan_name='Pro Plus (Trial)',
                            available_daily_corrections=4,
                            correction_type=Plan.CORRECTION_TYPE_PRO,
                            number_of_days=7,
                            price=100000000)

