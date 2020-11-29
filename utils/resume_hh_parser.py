import decimal
from datetime import timedelta
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.db.utils import IntegrityError
from parse_hh_data import download, parse  # noqa: WPS347

from recruitment.models import Candidate
from utils.datetime_parser import parse_date


def check_salary(salary):
    """Проверка длины строки."""
    return len(str(salary)) > 9


def get_response(url):
    """Получение данных по url."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
    }
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        return None
    return response


def get_hh_resume_ids():  # noqa: WPS210
    """Получение списка id резюме."""
    area_id = 113
    specialization_id = 1
    search_period = 360
    num_pages = 100
    list_resume = download.resume_ids(
        area_id=area_id,
        specialization_id=specialization_id,
        search_period=search_period,
        num_pages=num_pages,
    )
    with open('resume.txt', 'w', encoding='utf8') as resume_file:
        for row in list_resume:
            resume_file.write(row + '\n')  # noqa: WPS336


def get_hh_resume():  # noqa: WPS210, WPS231
    """Парсинг резюме с сайта hh."""
    resource_identifier = 'HH'
    url_hh = 'https://hh.ru/'
    list_resume = []
    with open('resume.txt', 'r') as resume_file:
        for row in resume_file:
            list_resume.append(row.rstrip())
    for resume in list_resume:
        source_id = resource_identifier + str(resume)
        raw_data = download.resume(resume)
        json_data = parse.resume(raw_data)

        resume_relative_url = f'/resume/{resume}?hhtmFrom=resume_search_result'
        resume_absolute_url = urljoin(url_hh, resume_relative_url)
        raw_resume = get_response(resume_absolute_url)
        if not raw_resume:
            break
        try:  # noqa: WPS229
            soup_resume = BeautifulSoup(raw_resume.text, 'lxml')
            rez = soup_resume.find('div', class_='bloko-columns-row')
            header = rez.find('div', class_='resume-header-title').find_all('p')
            ready_to_move = header[1].text.replace('\u2009', '').replace('\xa0', ' ').split(',')[-1]
            title_span = header[0].find_all('span')
            try:  # noqa: WPS505
                age = title_span[1].text.replace('\xa0', ' ').split(' ')[0]
            except (KeyError, ValueError):
                age = None
            description = soup_resume.find('div', class_='resume-wrapper')
            position = description.find(attrs={'class': 'resume-block', 'data-qa': 'resume-block-position'})
            working_conditions = position.find_all('p')
            work_schedule = working_conditions[0].text.replace('\u2009', '').replace('\xa0', ' ')  # TODO -> list
            type_of_work = working_conditions[1].text.replace('\u2009', '').replace('\xa0', ' ')  # TODO -> list
            expiriens = description.find(attrs={'class': 'resume-block', 'data-qa': 'resume-block-experience'})
            last_job = expiriens.find('div', class_='resume-block-container')
            last_employee = last_job.find(
                'div', class_='resume-block__sub-title',
            ).text.replace('\u2009', '').replace('\xa0', ' ')
        except AttributeError:
            pass  # noqa: WPS420

        gender = json_data['gender']
        city = json_data['area'].replace('\u2009', '').replace('\xa0', ' ')
        title = json_data['title'].replace('\u2009', '').replace('\xa0', ' ')
        if not check_salary(json_data['salary']['amount']):  # noqa: WPS504
            salary = json_data['salary']['amount']
        else:
            salary = None
        branch = json_data['specialization'][0]['profarea_name'].replace('\u2009', '').replace('\xa0', ' ')
        spec = json_data['specialization'][0]['name'].replace('\u2009', '').replace('\xa0', ' ')
        total_work_exp = timedelta()
        for date in json_data['experience']:  # noqa: WPS204, WPS519
            total_work_exp += parse_date(date['end']) - parse_date(date['start'])  # noqa: WPS519
        try:
            last_job_title = json_data['experience'][0]['position'].replace('\u2009', '').replace('\xa0', ' ')
        except (KeyError, TypeError):
            last_job_title = ''
        try:
            last_job_responsibilities = json_data['experience'][0]['description'].replace('\u2009', '').replace('\xa0', ' ')  # noqa: E501
        except (KeyError, TypeError):
            last_job_responsibilities = ''
        try:  # noqa: WPS229
            job_end_date = json_data['experience'][0]['end']
            job_start_date = json_data['experience'][0]['start']
        except (KeyError, TypeError):
            last_job_time = ''
        else:
            last_job_time = parse_date(job_end_date) - parse_date(job_start_date)

        skills = ''.join(json_data['skill_set']).replace('\u2009', '').replace('\xa0', ' ')
        about_candidate = json_data['skills'].replace('\u2009', '').replace('\xa0', ' ')
        education = json_data['education_level'].replace('\u2009', '').replace('\xa0', ' ')
        language_list = json_data['language']
        source = resume_absolute_url

        try:  # noqa WPS229
            candidate, created = Candidate.objects.get_or_create(
                gender=gender,
                age=age,
                city=city,
                ready_to_move=ready_to_move,
                title=title,
                salary=salary,
                branch=branch,
                spec=spec,
                type_of_work=type_of_work,
                work_schedule=work_schedule,
                total_work_exp=total_work_exp.days,
                last_employee=last_employee,
                last_job_title=last_job_title,
                last_job_responsibilities=last_job_responsibilities,
                last_job_time=last_job_time.days,
                skills=skills,
                about_candidate=about_candidate,
                education=education,
                source=source,
                source_id=source_id,
            )
            if created:
                for language in language_list:
                    candidate.language.name = language['name']
                    candidate.language.level = language['level']
                    candidate.save()
        except (IntegrityError, decimal.InvalidOperation):
            pass  # noqa: WPS420
