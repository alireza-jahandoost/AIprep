import pytz
import datetime
import difflib

from correction.models import QuestionTypeData


def get_number_of_today_corrections(user):
    today = datetime.datetime.today()
    today = datetime.datetime(today.year, today.month, today.day, 0, 0, 0, 0, pytz.UTC)
    return user.correction_set.filter(created_at__gt=today).count()

def get_supported_exams(exam_type, exam_db_name):
    exam_db_numbers = QuestionTypeData.objects.filter(exam_type=exam_type, exam_db_name=exam_db_name).values_list('exam_db_number')
    if len(exam_db_numbers) == 0:
        return 0, 0
    return min(exam_db_numbers)[0], max(exam_db_numbers)[0]

def get_supported_range_of_exam_message(exam_type, exam_db_name):
    exam_db_name_str = None
    for x in QuestionTypeData.EXAM_DB_CHOICES:
        if str(x[0]) == str(exam_db_name):
            exam_db_name_str = x[1]

    exam_type_str = None
    for x in QuestionTypeData.EXAM_TYPE_CHOICES:
        if str(x[0]) == str(exam_type):
            exam_type_str = x[1]

    minimum, maximum = get_supported_exams(exam_type, exam_db_name)

    if not minimum or not maximum:
        return f"{exam_db_name_str} of {exam_type_str} is not supported!"

    return f"{exam_type_str} of {exam_db_name_str} is supported from number {minimum} to {maximum}."

def make_not_in_range_error_message(exam_type, exam_db_name):
    return f"The specified exam is not supported! " + get_supported_range_of_exam_message(exam_type, exam_db_name)

def make_comparison(original_text, new_text):
    d = difflib.Differ()
    diff = list(d.compare(original_text.split(), new_text.split()))

    # Create HTML for the differences
    result = []
    for line in diff:
        if line.startswith('+ '):
            result.append(
                f'<span style="color: green;" class="font-weight-bold  text-decoration-underline">{line[2:]}</span>')
        elif line.startswith('- '):
            result.append(
                f'<span style="color: red;" class="font-weight-bold text-decoration-underline">{line[2:]}</span>')
        else:
            result.append(line[2:])  # lines that are the same

    # Join the results into a single HTML string
    diff_html = ' '.join(result)
    return diff_html
