import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.db.utils import IntegrityError

from utils.datetime_parser import parse_geekjob_date, parse_hh_date
from utils.models import Vacancy


def check_salary(salary):
    """Проверка длины строки."""
    return len(str(salary)) > 9


def get_geekjob_vacancy_snippet():
    """Получаем название и url вакансий."""
    site_url = 'https://geekjob.ru/'

    with open('vacancy_gj.html', 'r', encoding='utf8') as vacancies:
        html = vacancies.read()
    soup = BeautifulSoup(html, 'lxml')
    all_vacancies = soup.find('ul', class_='serp-list').findAll('li', class_='avatar')

    for vacancy in all_vacancies:
        title = vacancy.find('p', class_='vacancy-name').text
        relative_url = vacancy.find('p', class_='vacancy-name').find('a', class_='title')['href']
        absolute_url = urljoin(site_url, relative_url)
        Vacancy.objects.get_or_create(title=title, source=absolute_url)


def get_geekjob_full_vacancy():
    """получаем полные данные по вакансии."""
    resource_identifier = 'GJ'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
    }
    for vacancy in Vacancy.objects.filter(source_id=None):
        response = requests.get(vacancy.source, headers=headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            break
        soup = BeautifulSoup(response.text, 'lxml')
        try:  # noqa: WPS229
            raw_json = soup.find('script', type='application/ld+json').contents
            json_data = json.loads(''.join(raw_json))
        except json.decoder.JSONDecodeError:
            break
        else:
            vacancy.published_at = parse_geekjob_date(json_data.get('datePosted'))
            try:
                vacancy.source_id = resource_identifier + json_data['identifier']['value']
            except KeyError:
                vacancy.source_id = resource_identifier + str(vacancy.id)

            try:
                vacancy.description = json_data['description']
            except KeyError:
                vacancy.description = ''

            try:
                vacancy.employer_type = json_data['hiringOrganization']['@type']
            except KeyError:
                vacancy.employer_type = ''

            try:
                vacancy.employer_name = json_data['hiringOrganization']['name']
            except KeyError:
                vacancy.employer_name = ''

            try:
                vacancy.location_city = json_data['jobLocation']['address']['addressLocality']
            except KeyError:
                vacancy.location_city = ''

            try:
                vacancy.location_country = json_data['jobLocation']['address']['addressCountry']
            except KeyError:
                vacancy.location_country = ''
            salary = json_data['baseSalary']
            try:
                vacancy.salary_currency = salary['currency'] or ''
            except KeyError:
                vacancy.salary_currency = ''

            try:  # noqa: WPS229
                vacancy.salary_value = salary['value']['value']
                if check_salary(vacancy.salary_value):
                    raise ValueError
            except (KeyError, ValueError):
                vacancy.salary_value = None

            try:  # noqa: WPS229
                vacancy.salary_left_value = salary['value']['minValue']
                if check_salary(vacancy.salary_left_value):
                    raise ValueError
            except (KeyError, ValueError):
                vacancy.salary_left_value = None

            try:  # noqa: WPS229
                vacancy.salary_right_value = json_data['baseSalary']['value']['maxValue']
                if check_salary(vacancy.salary_right_value):
                    raise ValueError
            except (KeyError, ValueError):
                vacancy.salary_right_value = None

            try:
                vacancy.job_format = json_data['employmentType']
            except KeyError:
                vacancy.job_format = ''

            specialization = soup.find('div', class_='tags-list')
            skils = {}
            for parent in specialization.find_all('b'):
                skils[parent.text] = []
                for child in parent.next_siblings:
                    if child.name == 'a':
                        skils[parent.text] += [_.strip() for _ in child.text.split(',')]
                    elif child.name == 'b':
                        break
            try:
                vacancy.candidate_level = ','.join(skils.get('Уровень должности'))
            except TypeError:
                vacancy.candidate_level = ''
            try:
                vacancy.specialization = ','.join(skils.get('Специализация'))
            except TypeError:
                vacancy.specialization = ''
            try:
                vacancy.branch = ','.join(skils.get('Отрасль и сфера применения'))
            except TypeError:
                vacancy.branch = ''
            vacancy.save()


def get_json(url):
    """Получение json."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return json.loads(response.text)


def get_hh_full_vacancy():
    """Парсинг вакансий."""
    resource_identifier = 'HH'
    with open('vac-hh.html', 'r', encoding='utf8') as vacancies:
        html = vacancies.read()
    soup = BeautifulSoup(html, 'lxml')
    vacancies_ids = set()
    all_vacancies = soup.find_all('div', 'vacancy-serp-item__controls-item_response')
    for vacancy in all_vacancies:
        raw_data = vacancy.find('script')['data-params']
        vacancy_data = json.loads(raw_data)
        vacancies_ids.add(vacancy_data['vacancyId'])

    for row in vacancies_ids:
        vacancies_url = 'https://api.hh.ru/vacancies/'
        employers_url = 'https://api.hh.ru/employers/'
        vacancy_url = vacancies_url + str(row)
        vacancy_data = get_json(vacancy_url)
        try:  # noqa: WPS229
            employer_url = employers_url + str(vacancy_data['employer']['row'])
            employer = get_json(employer_url)
        except KeyError:
            employer = {'type': None}

        title = vacancy_data['name']
        published_at = parse_hh_date(vacancy_data['published_at'])
        source_id = resource_identifier + str(row)
        description = vacancy_data['description']
        employer_type = employer['type']
        employer_name = vacancy_data['employer']['name']
        location_city = vacancy_data['area']['name']
        location_country = 'planetEarth'
        salary_currency = vacancy_data['salary']['currency']  # noqa: WPS204
        salary_value = vacancy_data['salary']['from'] if not check_salary(vacancy_data['salary']['from']) else None  # noqa: WPS504
        salary_left_value = vacancy_data['salary']['from'] if not check_salary(vacancy_data['salary']['from']) else None  # noqa: WPS504
        salary_right_value = vacancy_data['salary']['to'] if not check_salary(vacancy_data['salary']['to']) else None  # noqa: WPS504
        if vacancy_data['schedule']['row'] == 'fullDay':
            job_format = 'FULL_TIME'
        elif vacancy_data['schedule']['row'] == 'part':
            job_format = 'PART_TIME'
        else:
            job_format = ''
        candidate_level = vacancy_data['experience']['row']
        specialization = ','.join([_['name'] for _ in vacancy_data['key_skills']])
        branch = vacancy_data['specializations'][0]['profarea_name']
        source = vacancy_data['alternate_url']
        try:
            Vacancy.objects.get_or_create(
                title=title,
                published_at=published_at,
                source_id=source_id,
                description=description,
                employer_type=employer_type,
                employer_name=employer_name,
                location_city=location_city,
                location_country=location_country,
                salary_currency=salary_currency,
                salary_value=salary_value,
                salary_left_value=salary_left_value,
                salary_right_value=salary_right_value,
                job_format=job_format,
                candidate_level=candidate_level,
                specialization=specialization,
                branch=branch,
                source=source,
            )
        except IntegrityError:
            pass  # noqa: WPS420


def get_response(url, payload=None):
    """Получение ответа на запрос."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
    }
    response = requests.get(url, headers=headers, params=payload)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return None
    return response


def get_habr_full_vacancy():
    """Получение полного списка вакансий."""
    resource_identifier = 'HB'
    all_vacancies = []
    for page in range(1, 3):
        payload = {
            'q': 'аналитик',
            'type': 'all',
            'with_salary': 'true',
            'page': page,
            'per_page': '100',
        }
        vacancy_url = 'https://career.habr.com/vacancies'
        vacancy_data = get_response(vacancy_url, payload)
        soup = BeautifulSoup(vacancy_data.text, 'lxml')
        vacancies = soup.find('ul', class_='card-list--appearance-within-section').find_all('li')

        for link in vacancies:
            all_vacancies.append(link.find('a', 'vacancy-card__icon-link')['href'])

    for vacancy in all_vacancies:
        site_url = 'https://career.habr.com/'
        vacancy_url = urljoin(site_url, vacancy)
        vacancy_data = get_response(vacancy_url)
        if not vacancy_data:
            break
        soup = BeautifulSoup(vacancy_data.text, 'lxml')
        try:  # noqa: WPS229
            raw_json = soup.find('script', type='application/ld+json').contents
            json_data = json.loads(''.join(raw_json), strict=False)
        except json.decoder.JSONDecodeError:
            break

        published_at = parse_hh_date(json_data.get('datePosted'))

        try:
            title = json_data['title']
        except KeyError:
            title = ''

        source_id = resource_identifier + str(vacancy.id)

        try:
            description = json_data['description']
        except KeyError:
            description = ''

        try:
            employer_type = json_data['hiringOrganization']['@type']
        except KeyError:
            employer_type = ''

        try:
            employer_name = json_data['hiringOrganization']['name']
        except KeyError:
            employer_name = ''

        if isinstance(json_data['jobLocation']['address'], dict):
            location_city = json_data['jobLocation']['address']['addressLocality']
            location_country = json_data['jobLocation']['address']['addressCountry']['name']
        else:
            location_city = json_data['jobLocation']['address']
            location_country = ''

        try:
            salary_currency = json_data['baseSalary']['currency'] or ''
        except KeyError:
            salary_currency = ''

        try:  # noqa: WPS229
            salary_value = json_data['baseSalary']['value']['value']
            if check_salary(salary_value):
                raise ValueError
        except (KeyError, ValueError):
            salary_value = None

        try:  # noqa: WPS229
            salary_left_value = json_data['baseSalary']['value']['minValue']
            if check_salary(salary_left_value):
                raise ValueError
        except (KeyError, ValueError):
            salary_left_value = None

        try:  # noqa: WPS229
            salary_right_value = json_data['baseSalary']['value']['maxValue']
            if check_salary(salary_right_value):
                raise ValueError
        except (KeyError, ValueError):
            salary_right_value = None

        try:
            job_format = json_data['employmentType']
        except KeyError:
            job_format = ''
        try:
            Vacancy.objects.get_or_create(
                title=title,
                published_at=published_at,
                source_id=source_id,
                description=description,
                employer_type=employer_type,
                employer_name=employer_name,
                location_city=location_city,
                location_country=location_country,
                salary_currency=salary_currency,
                salary_value=salary_value,
                salary_left_value=salary_left_value,
                salary_right_value=salary_right_value,
                job_format=job_format,
                source=vacancy_url,
            )
        except IntegrityError:
            pass  # noqa: WPS420
