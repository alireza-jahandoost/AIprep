from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseServerError
import requests
import json

from django.urls import reverse
from django.utils.decorators import method_decorator

from subscriptions.helper_functions import get_current_plan_of_user
from subscriptions.models import Plan, Payment

#? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

phone = 'YOUR_PHONE_NUMBER'  # Optional


# Important: need to edit for real server.


@login_required(login_url='login')
def show_plans(request):
    plans = Plan.objects.all()
    plan_of_the_user = get_current_plan_of_user(request.user)
    return render(request, 'show_plans.html',
                  {
                      'plans': plans,
                      'current_plan_of_user': plan_of_the_user,
                      'segment': 'plans',
                      'can_user_order': plan_of_the_user.plan_name.lower() == 'normal'})


@login_required(login_url='login')
def order(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)

    plan_of_the_user = get_current_plan_of_user(request.user)
    if plan_of_the_user.plan_name.lower() != 'normal' or plan.plan_name.lower() == 'normal':
        return HttpResponse("Forbidden", status=403)

    data = {
        "merchant_id": settings.MERCHANT,
        "amount": plan.price,
        "currency": "IRT",
        "description": f"خرید اشتراک {plan.plan_name} {plan.number_of_days} روزه",
        "callback_url": request.build_absolute_uri(reverse('verify', args=[plan.id])),
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response_json = response.json()
            authority = response_json['data']['authority']
            if response_json['data']['code'] == 100:
                return redirect(ZP_API_STARTPAY + authority)
            else:
                messages.error(request, 'خطایی رخ داده است (Repeated Request)' + str(response.status_code))
        else:
            messages.error(request, 'خطایی رخ داده است (Response Failed)' + str(response.status_code))
    except requests.exceptions.Timeout:
        messages.error(request, 'خطایی رخ داده است (Timeout Error)')
    except requests.exceptions.ConnectionError:
        messages.error(request, 'خطایی رخ داده است (Connection Error)')
    return redirect(reverse('subscription_transactions'))


@login_required(login_url='login')
def verify(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)

    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    if status == 'OK' and authority:
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": plan.price,
            "authority": authority,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
            if response.status_code == 200:
                response_json = response.json()
                if response_json['data']['code'] == 100:
                    Payment.objects.create(plan=plan,
                                           user=request.user,
                                           ref_id=response_json['data']['ref_id'],
                                           card_hash=response_json['data']['card_hash'],
                                           card_pan=response_json['data']['card_pan'],
                                           code=response_json['data']['code'],)
                    messages.success(request, "تراکنش با موفقیت انجام شد. ممنون که در این راه، مارا انتخاب کرده اید.")
                else:
                    messages.error(request, 'خطایی رخ داده است (Repeated Request)')
            else:
                messages.error(request, 'خطایی رخ داده است (Response Failed)')
        except requests.exceptions.Timeout:
            messages.error(request, 'خطایی رخ داده است (Timeout Error)')
        except requests.exceptions.ConnectionError:
            messages.error(request, 'خطایی رخ داده است (Connection Error)')
    else:
        messages.error(request, 'تراکنش ناموفق بود')

    return redirect(reverse('subscription_transactions'))


@login_required(login_url='login')
def transactions(request):
    transactions = Payment.objects.filter(user=request.user).all().order_by('-created_at')
    # breakpoint()
    return render(request, 'transactions.html', {
        'transactions': transactions,
        'number_of_transactions': len(transactions),
        'segment': 'transactions',
    })
