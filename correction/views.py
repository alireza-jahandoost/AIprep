from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from correction.forms import form_validation_error, ToeflWritingForm
from correction.models import Correction, QuestionTypeData


# import pdb
# pdb.set_trace()

@method_decorator(login_required(login_url='login'), name='dispatch')
class CreateToeflIntegratedView(View):
    next_url = "create_integrated"
    correction = None

    def dispatch(self, request, *args, **kwargs):
        return super(CreateToeflIntegratedView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'toefl/create_integrated.html')

    def post(self, request):
        form = ToeflWritingForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                question_type_data = QuestionTypeData.objects.get(exam_type=QuestionTypeData.EXAM_TYPE_TOEFL_TASK1,
                                                                  exam_db_name=form.cleaned_data['exam_db_name'],
                                                                  exam_db_number=form.cleaned_data['exam_db_number'])

            except:
                messages.error(request, "The specified exam is not supported! TPO 40-75 and NEO 01-40 are supported.")
                context = {
                    'exam_db_name': form.cleaned_data['exam_db_name'],
                    'exam_db_number': form.cleaned_data['exam_db_number'],
                    'answer': form.cleaned_data['answer'],
                }
                return render(request, 'toefl/create_integrated.html', context)

            correction = Correction(user=request.user,
                                    question_type_data=question_type_data,
                                    answer=form.cleaned_data['answer'])
            correction.save()

            messages.success(request, 'Correction submitted successfully')
        else:
            messages.error(request, form_validation_error(form))
        return render(request, 'toefl/create_integrated.html')

@method_decorator(login_required(login_url='login'), name='dispatch')
class CreateToeflIndependentView(View):
    next_url = "create_independent"
    correction = None

    def dispatch(self, request, *args, **kwargs):
        return super(CreateToeflIndependentView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'toefl/create_independent.html')

    def post(self, request):
        form = ToeflWritingForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                question_type_data = QuestionTypeData.objects.get(exam_type=QuestionTypeData.EXAM_TYPE_TOEFL_TASK2,
                                                                  exam_db_name=form.cleaned_data['exam_db_name'],
                                                                  exam_db_number=form.cleaned_data['exam_db_number'])

            except:
                messages.error(request, "The specified exam is not supported! NEO 01-10 is supported.")
                context = {
                    'exam_db_name': form.cleaned_data['exam_db_name'],
                    'exam_db_number': form.cleaned_data['exam_db_number'],
                    'answer': form.cleaned_data['answer'],
                }
                return render(request, 'toefl/create_independent.html', context)

            correction = Correction(user=request.user,
                                    question_type_data=question_type_data,
                                    answer=form.cleaned_data['answer'])
            correction.save()

            messages.success(request, 'Correction submitted successfully')
        else:
            messages.error(request, form_validation_error(form))
        return render(request, 'toefl/create_independent.html')


@login_required(login_url='login')
def ShowCorrectionsView(request):
    corrections = Correction.objects.filter(user=request.user)
    return render(request, 'show_corrections.html', {'corrections': corrections})
@login_required(login_url='login')
def ShowCorrectionView(request, correction_id):
    correction = get_object_or_404(Correction, pk=correction_id)
    if correction.correction is None or correction.get_status_display() == "Invalid":
        return render(request, '../../core/templates/page-404.html')
    return render(request, 'show_correction.html', {'correction': correction})