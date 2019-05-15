import os
from pprint import pprint
from time import sleep

from dotenv import load_dotenv
from terminaltables import AsciiTable
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


def get_salary_from_vacancies(vacancies_list, func_predict):
    salary = []
    for vacancy in vacancies_list:
        salary.append(func_predict(vacancy))
    return salary


def get_average_salary(salaries):
    salaries = [salary for salary in salaries if salary]
    try:
        average_salary = sum(salaries) / len(salaries)
    except ZeroDivisionError:
        return 0

    return int(average_salary)


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
        sleep(0.5)
        page_number = vacancy_info['pages']
        page += 1
        vacancies['items'].extend(vacancy_info['items'])
        if not vacancies.get('found'):
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
        if not vacancies.get('found'):
            vacancies['found'] = vacancy_info['total']
    return vacancies


def get_hh_vacancy_info(vacancy):
    vacancies = get_all_hh_vacancies(vacancy)
    vacancies_salary = get_salary_from_vacancies(vacancies['items'], get_predict_rub_salary_hh)
    vacancy_info = {
        "vacancies_found": vacancies['found'],
        "vacancies_processed": len(list(filter(lambda x: x, vacancies_salary))),
        "average_salary": get_average_salary(vacancies_salary)
    }
    return vacancy_info


def get_sj_vacancy_info(vacancy):
    vacancies = get_all_sj_vacancies(vacancy)
    vacancies_salary = get_salary_from_vacancies(vacancies['items'], get_predict_rub_salary_sj)
    vacancy_info = {
        "vacancies_found": vacancies['found'],
        "vacancies_processed": len(list(filter(lambda x: x, vacancies_salary))),
        "average_salary": get_average_salary(vacancies_salary)
    }
    return vacancy_info


def formate_table(vacancies_info):
    table_header = ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    table_data = [
        table_header,
    ]
    for vacancy, vacancies_info in vacancies_info.items():
        table_row = [vacancy,
                     vacancies_info['vacancies_found'],
                     vacancies_info['vacancies_processed'],
                     vacancies_info['average_salary']
                     ]
        table_data.append(table_row)
    return table_data


def main():
    vacancies_list = [
        'JavaScript',
        'Java',
        'Python',
        'Kotlin',
        'Swift',
        'PHP'
    ]
    result_sj = {}
    result_hh = {}
    for vacancy in vacancies_list:
        result_hh[vacancy] = get_hh_vacancy_info(vacancy)
        result_sj[vacancy] = get_sj_vacancy_info(vacancy)

    hh_info_table = formate_table(result_hh)
    sj_info_table = formate_table(result_sj)

    hh_table = AsciiTable(hh_info_table)
    sj_table = AsciiTable(sj_info_table)

    print(hh_table.table)
    print(sj_table.table)


if __name__ == '__main__':
    main()
