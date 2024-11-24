# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import os
import random

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone
from requests import HTTPError

from authentication.models import CustomUser as User
from django.forms.utils import ErrorList
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from sms_ir import SmsIr

from subscriptions.helper_functions import is_subscription_code_valid
from subscriptions.models import Plan, Payment, SubscriptionCode
from .forms import LoginForm, SignUpForm

def convert_persian_number_to_english(number):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"

    output = ""

    for digit in number:
        if digit in persian_digits:
            idx = persian_digits.index(digit)
            output += english_digits[idx]
        else:
            output += digit

    return output

def send_otp(code, phone_number):
    sms_ir = SmsIr(api_key=os.environ.get('SMS_IR_API_KEY'), linenumber=os.environ.get('SMS_IR_LINENUMBER'))
    response = sms_ir.send_verify_code(number=phone_number,
                            template_id=os.environ.get('SMS_IR_TEMPLATE_ID'),
                            parameters=[
                                {
                                    "name": "code",
                                    "value": code,
                                }
                            ])
    return response.json()['status'] == 1

def login_view(request):
    AUTHENTICATED_REDIRECT_NAME = 'dashboard'

    if request.user.is_authenticated:
        return redirect(AUTHENTICATED_REDIRECT_NAME)

    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":
        if form.is_valid():
            phone_number_user_name = form.cleaned_data.get("phone_number_user_name")
            phone_number_user_name = convert_persian_number_to_english(phone_number_user_name)
            user = None
            try:
                user = User.objects.filter(username=phone_number_user_name).get()
            except:
                pass
            if user is not None:

                # For testing
                if os.getenv('DEBUG', False) and user.username == '09156197717':
                    login(request, user)
                    return redirect(AUTHENTICATED_REDIRECT_NAME)
                # End for testing

                is_there_valid_otp = False
                if user.otp_creation and ((timezone.now() - user.otp_creation).seconds < 300):
                    is_there_valid_otp = True
                if is_there_valid_otp:
                    if form.cleaned_data.get("otp_code") != "":
                        otp_code = form.cleaned_data.get("otp_code")
                        if user.check_password(otp_code):
                            login(request, user)
                            return redirect(AUTHENTICATED_REDIRECT_NAME)
                        else:
                            msg = 'Invalid OTP Code'

                    return render(request, "accounts/otp.html", {
                        "form": form,
                        "msg": msg,
                        "phone_number_user_name": user.username,
                    })
                else:
                    otp_password = random.randint(100000, 999999)
                    user.set_password(otp_password)
                    user.otp_creation = timezone.now()
                    user.save()
                    if send_otp(otp_password, user.username):
                        msg = 'OTP code has been sent.'
                    return render(request, "accounts/otp.html", {
                        "form": form,
                        "msg": msg,
                        "phone_number_user_name": user.username,
                    })
            else:
                msg = 'Invalid Credentials'
        else:
            msg = 'Invalid Credentials'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False
    error = False
    subscription_code = None

    if request.method == "POST":

        # For maintenance settings
        if os.getenv('IS_REGISTRATION_CLOSED', False):
            return HttpResponseForbidden("Registration is not open currently (maintenance)")
        # End for maintenance settings

        form = SignUpForm(request.POST)
        if form.is_valid():
            # form.save()
            phone_number_user_name = form.cleaned_data.get("phone_number_user_name")
            phone_number_user_name = convert_persian_number_to_english(phone_number_user_name)
            subscription_code = form.cleaned_data.get("subscription_code")
            if User.objects.filter(username=phone_number_user_name).exists():
                msg = 'User with this phone number already exists. Try to login.'
                error = True
            else:
                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                user = User.objects.create(username=phone_number_user_name,
                                           first_name=first_name,
                                           last_name=last_name)

                # Activate trial
                if subscription_code and is_subscription_code_valid(subscription_code):
                    subscription_plan = SubscriptionCode.objects.filter(code=subscription_code).get().plan
                    Payment.objects.create(user=user,
                                           plan=subscription_plan,
                                           discount_or_subscription_code=subscription_code,
                                           hide_payment=True)
                else:
                    trial_plan = Plan.objects.filter(plan_name='Pro Plus (Trial)').get()
                    Payment.objects.create(
                        user=user,
                        plan=trial_plan,
                        hide_payment=True,
                    )
                # End activate trial

                msg = 'User created - please <a href="/login">login</a>.'
                success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
            subscription_code = form.cleaned_data.get("subscription_code")
            error = True
    else:
        form = SignUpForm()
        subscription_code = request.GET.get('subscription_code')
        if subscription_code is not None:
            subscription_code = subscription_code.encode('ascii', 'ignore').decode('ascii')

    return render(request, "accounts/register.html", {
        "form": form,
        "msg": msg,
        "success": success,
        "error": error,
        'subscription_code': subscription_code,
    })
