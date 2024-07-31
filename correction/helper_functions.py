import pytz
import datetime


def get_number_of_today_corrections(user):
    today = datetime.datetime.today()
    today = datetime.datetime(today.year, today.month, today.day, 0, 0, 0, 0, pytz.UTC)
    return user.correction_set.filter(created_at__gt=today).count()
