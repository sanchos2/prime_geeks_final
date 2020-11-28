import requests
import decimal
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from parse_hh_data import download, parse
from datetime import datetime, timedelta
from django.db.utils import IntegrityError
from recruitment.models import Candidate


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d-%m-%Y')
    except (ValueError, TypeError):
        return datetime.now()


def check_salary(salary):
    return len(str(salary)) > 9


def get_response(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    }
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
    except Exception as e:
        return None
    return response


def get_hh_resume_ids():
    list_resume = download.resume_ids(area_id=113, specialization_id=1, search_period=360, num_pages=100)
    with open('resume.txt', 'w', encoding='utf8') as file:
        for id in list_resume:
            file.write(id + '\n')


def get_hh_resume():
    resource_identifier = 'HH'
    url_hh = 'https://hh.ru/'
    list_resume = []
    with open('resume.txt', 'r') as file:
        for row in file:
            list_resume.append(row.rstrip())
    print(list_resume)
    for resume in list_resume:
        source_id = resource_identifier + str(resume)
        raw_data = download.resume(resume)
        json_data = parse.resume(raw_data)

        resume_relative_url = f'/resume/{resume}?hhtmFrom=resume_search_result'
        resume_absolute_url = urljoin(url_hh, resume_relative_url)
        raw_resume = get_response(resume_absolute_url)
        if not raw_resume:
            break
        try:
            soup_resume = BeautifulSoup(raw_resume.text, 'lxml')
            rez = soup_resume.find('div', class_='bloko-columns-row')
            header = rez.find('div', class_='resume-header-title').find_all('p')
            ready_to_move = header[1].text.replace('\u2009', '').replace('\xa0', ' ').split(',')[-1]
            title_span = header[0].find_all('span')
            try:
                age = title_span[1].text.replace('\xa0', ' ').split(' ')[0]
            except Exception as e:
                age = None
            description = soup_resume.find('div', class_='resume-wrapper')
            position = description.find(attrs={'class': 'resume-block', 'data-qa': 'resume-block-position'})
            working_conditions = position.find_all('p')
            work_schedule = working_conditions[0].text.replace('\u2009', '').replace('\xa0', ' ')  # TODO -> list
            type_of_work = working_conditions[1].text.replace('\u2009', '').replace('\xa0', ' ')  # TODO -> list
            expiriens = description.find(attrs={'class': 'resume-block', 'data-qa': 'resume-block-experience'})
            last_job = expiriens.find('div', class_='resume-block-container')
            last_employee = last_job.find('div', class_='resume-block__sub-title').text.replace('\u2009', '').replace(
                '\xa0', ' ')
        except AttributeError:
            pass

        gender = json_data['gender']
        city = json_data['area'].replace('\u2009', '').replace('\xa0', ' ')
        title = json_data['title'].replace('\u2009', '').replace('\xa0', ' ')
        salary = json_data['salary']['amount'] if not check_salary(json_data['salary']['amount']) else None
        branch = json_data['specialization'][0]['profarea_name'].replace('\u2009', '').replace('\xa0', ' ')
        spec = json_data['specialization'][0]['name'].replace('\u2009', '').replace('\xa0', ' ')
        total_work_exp = timedelta()
        for i in json_data['experience']:
            total_work_exp += parse_date(i['end']) - parse_date(i['start'])
        try:
            last_job_title = json_data['experience'][0]['position'].replace('\u2009', '').replace('\xa0', ' ')
        except Exception as e:
            pass
        try:
            last_job_responsibilities = json_data['experience'][0]['description'].replace('\u2009', '').replace('\xa0', ' ')
        except Exception as e:
            pass
        try:
            last_job_time = parse_date(json_data['experience'][0]['end']) - parse_date(json_data['experience'][0]['start'])
        except Exception as e:
            pass
        skills = ''.join(json_data['skill_set']).replace('\u2009', '').replace('\xa0', ' ')
        about_candidate = json_data['skills'].replace('\u2009', '').replace('\xa0', ' ')
        education = json_data['education_level'].replace('\u2009', '').replace('\xa0', ' ')
        language_list = json_data['language']
        source = resume_absolute_url

        try:
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
            print(candidate, created)
            if created:
                for language in language_list:
                    candidate.language.name = language['name']
                    candidate.language.level = language['level']
                    candidate.save()
        except (IntegrityError, decimal.InvalidOperation):
            pass
