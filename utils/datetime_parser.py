from datetime import datetime
from dateutil import parser
import locale
import platform

from django.utils import timezone

if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, 'russian')
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


def parse_geekjob_date(date_str):
    """Парсер текстового значения даты."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return timezone.now()


def parse_hh_date(date_str):
    """Парсер текстового значения даты."""
    try:
        return parser.parse(date_str)
    except ValueError:
        return timezone.now()


def parse_date(date_str):
    """Парсер текстового значения даты."""
    try:
        return datetime.strptime(date_str, '%d-%m-%Y')
    except (ValueError, TypeError):
        return datetime.now()
