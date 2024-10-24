import pytz
import datetime

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

def make_not_in_range_error_message(exam_type, exam_db_name):
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

    return f"The specified exam is not supported! {exam_db_name_str} of {exam_type_str} is supported from {minimum} to {maximum}."
# TODO: fix error in this file