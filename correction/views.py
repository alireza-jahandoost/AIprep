import re
from io import BufferedIOBase

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponse, FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from six import BytesIO

from correction.forms import form_validation_error, ToeflWritingForm
from correction.helper_functions import get_number_of_today_corrections, make_not_in_range_error_message, \
    get_supported_range_of_exam_message, make_comparison
from correction.models import Correction, QuestionTypeData
from correction.templatetags.markdown_extras import render_markdown
from subscriptions.helper_functions import get_current_plan_of_user

from xhtml2pdf import pisa

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
    if request.user.correction_set.filter(pk=correction_id).exists():
        correction = Correction.objects.get(pk=1)
    else:
        return HttpResponseNotFound()

    context = {
                  'correction': correction,
                  'segment': 'corrections'
              }

    if correction.correction is not None and correction.status == Correction.STATUS_CORRECTED:
        try:
            original_text = correction.answer
            revised_text = re.search(r"\*\*Revised Essay \(30\/30 Points\):\*\*(.*?)---", correction.correction, re.DOTALL).group(1).strip()
            comparison_html = make_comparison(original_text, revised_text)
            context['comparison'] = comparison_html
        except Exception as e:
            pass
    return render(request, 'show_correction.html', context)



@login_required(login_url='login')
def generate_pdf_from_template(request, correction_id):
    if request.user.correction_set.filter(pk=correction_id).exists():
        correction = Correction.objects.get(pk=correction_id)
        if correction.status != Correction.STATUS_CORRECTED:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()

    comparison_html = ""
    try:
        original_text = correction.answer
        revised_text = re.search(r"\*\*Revised Essay \(30\/30 Points\):\*\*(.*?)---", correction.correction, re.DOTALL).group(1).strip()
        comparison_html = make_comparison(original_text, revised_text)
    except Exception as e:
        pass

    with open("correction/data/pdf_templates/plain.html") as f:
        full_html = f.read()
        full_html = full_html.replace("[MAIN TEXT]", render_markdown(correction.correction) +
                                                            comparison_html)
    file = BytesIO()
    pisa.CreatePDF(
        full_html,
        dest=file,
    )
    response = HttpResponse(file.getbuffer().tobytes(), content_type='application/pdf')
    file_name = ('Report of ' +
                 correction.user.get_full_name() + " (" +
                 correction.question_type_data.get_exam_db_name_display() +
                 str(correction.question_type_data.exam_db_number) + ")")
    response['Content-Disposition'] = 'attachment; filename="' + file_name + '.pdf"'
    return response