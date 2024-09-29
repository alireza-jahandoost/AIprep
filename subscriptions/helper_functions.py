import time

from subscriptions.models import Plan

def get_last_payment_of_user(user):
    last_payment = user.payment_set.order_by('-created_at').first()
    return last_payment

def get_current_plan_of_user(user):
    last_payment = get_last_payment_of_user(user)
    if (last_payment is not None) and (last_payment.created_at.timestamp() > time.time() - last_payment.plan.number_of_days * 24 * 3600):
        return last_payment.plan
    else:
        return Plan.objects.filter(plan_name='Normal').get()
