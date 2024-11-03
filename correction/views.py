import difflib
import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from correction.forms import form_validation_error, ToeflWritingForm
from correction.helper_functions import get_number_of_today_corrections, make_not_in_range_error_message, \
    get_supported_range_of_exam_message
from correction.models import Correction, QuestionTypeData
from subscriptions.helper_functions import get_current_plan_of_user


# import pdb
# pdb.set_trace()

@method_decorator(login_required(login_url='login'), name='dispatch')
class CreateToeflIntegratedView(View):
    next_url = "create_integrated"
    correction = None
    tpo_range = None
    neo_range = None
    plan = None
    rem_corrections = None

    def __init__(self, *args, **kwargs):
        self.tpo_range = get_supported_range_of_exam_message(QuestionTypeData.EXAM_TYPE_TOEFL_TASK1, QuestionTypeData.EXAM_DB_TPO)
        self.neo_range = get_supported_range_of_exam_message(QuestionTypeData.EXAM_TYPE_TOEFL_TASK1, QuestionTypeData.EXAM_DB_NEO)

    def calc_plan_and_rem_corrections(self, user):
        self.plan = get_current_plan_of_user(user)
        self.rem_corrections = max(0, self.plan.available_daily_corrections - get_number_of_today_corrections(user))

    def dispatch(self, request, *args, **kwargs):
        return super(CreateToeflIntegratedView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        self.calc_plan_and_rem_corrections(request.user)

        return render(request, 'toefl/create_integrated.html',
                      {
                          'segment': 'toefl_writing_integrated',
                          'rem_corrections': self.rem_corrections,
                          'tpo_range': self.tpo_range,
                          'neo_range': self.neo_range,
                      })

    def post(self, request):
        self.calc_plan_and_rem_corrections(request.user)
        if get_number_of_today_corrections(request.user) >= self.plan.available_daily_corrections:
            return HttpResponse("Forbidden", status=403)

        form = ToeflWritingForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                question_type_data = QuestionTypeData.objects.get(exam_type=QuestionTypeData.EXAM_TYPE_TOEFL_TASK1,
                                                                  exam_db_name=form.cleaned_data['exam_db_name'],
                                                                  exam_db_number=form.cleaned_data['exam_db_number'])

            except:
                messages.error(request, make_not_in_range_error_message(QuestionTypeData.EXAM_TYPE_TOEFL_TASK1, form.cleaned_data['exam_db_name'],))
                context = {
                    'exam_db_name': form.cleaned_data['exam_db_name'],
                    'exam_db_number': form.cleaned_data['exam_db_number'],
                    'answer': form.cleaned_data['answer'],
                    'tpo_range': self.tpo_range,
                    'neo_range': self.neo_range,
                    'rem_corrections': self.rem_corrections,
                }
                return render(request, 'toefl/create_integrated.html', context)

            correction = Correction(user=request.user,
                                    question_type_data=question_type_data,
                                    answer=form.cleaned_data['answer'])
            correction.save()

            messages.success(request, 'Correction submitted successfully')
        else:
            messages.error(request, form_validation_error(form))
        return redirect(reverse('create_toefl_integrated'))

@method_decorator(login_required(login_url='login'), name='dispatch')
class CreateToeflIndependentView(View):
    next_url = "create_independent"
    correction = None
    tpo_range = None
    neo_range = None
    plan = None
    rem_corrections = None

    def __init__(self, *args, **kwargs):
        # self.tpo_range = get_supported_range_of_exam_message(QuestionTypeData.EXAM_TYPE_TOEFL_TASK2, QuestionTypeData.EXAM_DB_TPO)
        self.neo_range = get_supported_range_of_exam_message(QuestionTypeData.EXAM_TYPE_TOEFL_TASK2, QuestionTypeData.EXAM_DB_NEO)

    def calc_plan_and_rem_corrections(self, user):
        self.plan = get_current_plan_of_user(user)
        self.rem_corrections = max(0, self.plan.available_daily_corrections - get_number_of_today_corrections(user))

    def dispatch(self, request, *args, **kwargs):
        return super(CreateToeflIndependentView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        self.calc_plan_and_rem_corrections(request.user)
        return render(request, 'toefl/create_independent.html',
                      {
                          'segment': 'toefl_writing_independent',
                          'rem_corrections': self.rem_corrections,
                          'neo_range': self.neo_range,
                      })

    def post(self, request):
        self.calc_plan_and_rem_corrections(request.user)
        if get_number_of_today_corrections(request.user) >= self.plan.available_daily_corrections:
            return HttpResponse("Forbidden", status=403)

        form = ToeflWritingForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                question_type_data = QuestionTypeData.objects.get(exam_type=QuestionTypeData.EXAM_TYPE_TOEFL_TASK2,
                                                                  exam_db_name=form.cleaned_data['exam_db_name'],
                                                                  exam_db_number=form.cleaned_data['exam_db_number'])

            except:
                messages.error(request, make_not_in_range_error_message(QuestionTypeData.EXAM_TYPE_TOEFL_TASK2, form.cleaned_data['exam_db_name'],))
                context = {
                    'exam_db_name': form.cleaned_data['exam_db_name'],
                    'exam_db_number': form.cleaned_data['exam_db_number'],
                    'answer': form.cleaned_data['answer'],
                    'neo_range': self.neo_range,
                    'rem_corrections': self.rem_corrections,
                }
                return render(request, 'toefl/create_independent.html', context)

            correction = Correction(user=request.user,
                                    question_type_data=question_type_data,
                                    answer=form.cleaned_data['answer'])
            correction.save()

            messages.success(request, 'Correction submitted successfully')
        else:
            messages.error(request, form_validation_error(form))
        return redirect(reverse('create_toefl_independent'))


@login_required(login_url='login')
def ShowCorrectionsView(request):
    corrections = Correction.objects.filter(user=request.user)
    paginator = Paginator(corrections, 25)
    url_page_number = request.GET.get('page')
    page_number = 1
    if url_page_number and url_page_number.isdigit():
        page_number = int(url_page_number)
    corrections_object = paginator.get_page(page_number)

    return render(request, 'show_corrections.html', {
        'corrections_object': corrections_object,
        'page_range': paginator.page_range,
        'current_page': page_number,
        'segment': 'corrections',
        'number_of_corrections': len(corrections),
    })
@login_required(login_url='login')
def ShowCorrectionView(request, correction_id):
    correction = get_object_or_404(Correction, pk=correction_id)
    context = {
                  'correction': correction,
                  'segment': 'corrections'
              }

    if correction.correction is not None and correction.status == Correction.STATUS_CORRECTED:
        try:
            revised_text = re.search(r"\*\*Revised Essay \(30\/30 Points\):\*\*(.*?)---", correction.correction, re.DOTALL).group(1).strip()
            d = difflib.Differ()
            diff = list(d.compare(correction.answer.split(), revised_text.split()))

            # Create HTML for the differences
            result = []
            for line in diff:
                if line.startswith('+ '):
                    result.append(f'<span style="color: green;" class="font-weight-bold  text-decoration-underline">{line[2:]}</span>')
                elif line.startswith('- '):
                    result.append(f'<span style="color: red;" class="font-weight-bold text-decoration-underline">{line[2:]}</span>')
                else:
                    result.append(line[2:])  # lines that are the same

            # Join the results into a single HTML string
            diff_html = ' '.join(result)
            context['comparison'] = diff_html
        except Exception as e:
            pass
    return render(request, 'show_correction.html', context)