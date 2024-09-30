# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import datetime
from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.utils import timezone

from correction.helper_functions import get_number_of_today_corrections
from subscriptions.helper_functions import get_current_plan_of_user, get_last_payment_of_user

@login_required(login_url="/login/")
def dashboard(request):
    user_plan = get_current_plan_of_user(request.user)
    user_last_payment = get_last_payment_of_user(request.user)
    corrections = request.user.correction_set.order_by('-created_at')[:5]

    context = {
        'segment': 'dashboard',
        'user_plan': user_plan,
        'remaining_corrections': max(0, user_plan.available_daily_corrections - get_number_of_today_corrections(request.user)),
        'corrections': corrections,
        'number_of_corrections': len(corrections),
    }
    if user_last_payment:
        context['start_of_plan'] = user_last_payment.created_at.strftime('%b %d')
        context['end_of_plan'] = (user_last_payment.created_at + datetime.timedelta(days=user_plan.number_of_days)).strftime('%b %d')
        context['remaining_days'] = ((user_last_payment.created_at + datetime.timedelta(days=user_plan.number_of_days)) - timezone.now()).days
    return render(request, "dashboard.html", context)