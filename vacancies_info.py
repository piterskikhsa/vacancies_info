import os

from dotenv import load_dotenv
import requests


load_dotenv()


def is_salary_rub(vacancy_salary, currency):
    return vacancy_salary['currency'] == currency


def get_predict_salary(salary_from, salary_to):
    if salary_to and salary_from:
        return (salary_to + salary_from) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    else:
        return None


def get_vacancies(url, parameters, header=None):
    response = requests.get(url, params=parameters, headers=header)
    response.raise_for_status()
    return response.json()


def get_predict_rub_salary_hh(vacancy):
    salary = vacancy['salary']
    if not salary or not is_salary_rub(salary, 'RUR'):
        return None
    return get_predict_salary(salary['from'], salary['to'])


def get_predict_rub_salary_sj(vacancy):
    if not is_salary_rub(vacancy, 'rub'):
        return None
    return get_predict_salary(vacancy['payment_from'], vacancy['payment_to'])


def get_vacancies_found(vacancies):
    pass


def get_vacancies_processed(vacancies):
    pass


def get_average_salary(vacancies):
    pass


def get_all_hh_vacancies(search_vacancy):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'area': 1,
        'period': 30,
        'text': search_vacancy.lower()
    }
    page = 0
    page_number = 1
    vacancies = {
        'items': []
    }
    while page < page_number:
        params['page'] = page
        vacancy_info = get_vacancies(url, params)
        page_number = vacancy_info['pages']
        page += 1
        vacancies['items'].extend(vacancy_info['items'])
        if not vacancies['found']:
            vacancies['found'] = vacancy_info['found']
    return vacancies


def get_all_sj_vacancies(search_vacancy):
    headers = {'X-Api-App-Id': os.getenv('SECRET_KEY')}
    url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {
        'town': 4,
        'keyword': search_vacancy.lower()
    }
    page = 0
    page_number = 1
    page_number_not_calc = True
    vacancies = {
        'items': []
    }
    while page < page_number:
        params['page'] = page
        vacancy_info = get_vacancies(url, params, headers)
        if page_number_not_calc:
            page_number = int(vacancy_info['total'] // 20)
            page_number_not_calc = False
        page += 1
        vacancies['items'].extend(vacancy_info['objects'])
        if not vacancies['found']:
            vacancies['found'] = vacancy_info['total']
    return vacancies


def get_hh_vacancy_info(vacancy):
    vacancies = get_all_hh_vacancies(vacancy)
    vacancy_info = {
        "vacancies_found": vacancies['found'],
        "vacancies_processed": get_vacancies_processed(vacancies),
        "average_salary": get_average_salary(vacancies)
    }
    return vacancy_info


def get_sj_vacancy_info(vacancy):
    vacancies = get_all_sj_vacancies(vacancy)
    vacancy_info = {
        "vacancies_found": vacancies['total'],
        "vacancies_processed": get_vacancies_processed(vacancies),
        "average_salary": get_average_salary(vacancies)
    }
    return vacancy_info


def main():
    vacancies_list = [
        'JavaScript',
        'Java',
        'Python',
        'Kotlin',
        'Swift',
        'PHP'
    ]


if __name__ == '__main__':
    main()
