import logging
import time

from django.utils import timezone

from subscriptions.models import Plan, SubscriptionCode, Payment


def get_last_payment_of_user(user):
    last_payment = user.payment_set.order_by('-created_at').first()
    return last_payment

def get_current_plan_of_user(user):
    last_payment = get_last_payment_of_user(user)
    if (last_payment is not None) and (last_payment.created_at.timestamp() > time.time() - last_payment.plan.number_of_days * 24 * 3600):
        return last_payment.plan
    else:
        return Plan.objects.filter(plan_name='Normal').get()

def log_error(error_message):
    logging.getLogger("ERROR").error(error_message)

def is_subscription_code_valid(subscription_code):
    if isinstance(subscription_code, str):
        if not SubscriptionCode.objects.filter(code=subscription_code).exists():
            return False
        subscription_code_instance = SubscriptionCode.objects.get(code=subscription_code)
    else:
        subscription_code_instance = subscription_code

    is_valid = subscription_code_instance.expires_at is None or subscription_code_instance.expires_at > timezone.now()
    is_not_full = subscription_code_instance.number_of_usages > \
                  Payment.objects.filter(discount_or_subscription_code=subscription_code_instance.code).count()

    return is_valid and is_not_full