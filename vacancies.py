import requests
from dotenv import load_dotenv


load_dotenv()


languages = [
    'JavaScript',
    'Java',
    'Python',
]


def get_vacancies_for_languages(languages_list, request_url, par):
    vacancies_for_language = {}
    for language in languages_list:
        vacancies = get_vacancies_lang(request_url, par)
        vacancies_for_language[language] = vacancies["found"]

    return vacancies_for_language


def get_vacancies_lang(api_url, parameters):
    response = requests.get(api_url, params=parameters)
    response.raise_for_status()
    return response.json()


def get_salary_vacancies(vacancies):
    salaries = []
    for vacancy in vacancies['items']:
        salaries.append(vacancy['salary'])
    return salaries


# def predict_rub_salary(vacancy):
#     if not is_salary_currency(vacancy, 'RUR'):
#         return None
#     return calculate_salary(vacancy['salary'])
#
#
# def is_salary_currency(vacancy, currency):
#     vacancy_salary = vacancy['salary']
#     if not vacancy_salary:
#         return False
#     return vacancy_salary['currency'] == currency


def calculate_salary(salary):
    if salary['to'] and salary['from']:
        return (salary['to'] + salary['from']) / 2
    elif not salary['from']:
        return salary['to'] * 0.8
    else:
        return salary['from'] * 1.2


def calculate_average_salary(salaries):
    salaries = [salary for salary in salaries if salary]
    average_salary = sum(salaries) / len(salaries)
    return int(average_salary)


def get_all_vacancies_lang(url, params):
    page = 0
    page_number = 1
    vacancies = {
        'items': []
    }
    while page < page_number:
        params['page'] = page
        page_data = get_vacancies_lang(url, params)
        page_number = page_data['pages']
        page += 1
        vacancies['items'].extend(page_data['items'])
    vacancies['found'] = page_data['found']
    return vacancies


def get_lang_data(language):
    url = ' https://api.hh.ru/vacancies'
    params = {
        'area': 1,
        'period': 30,
        'text': language.lower()
    }
    vacancies = get_all_vacancies_lang(url, params)
    salaries = []
    lang_data = {
        'vacancies_found': vacancies['found']
    }

    for vac in vacancies['items']:
        salaries.append(predict_rub_salary(vac))
    lang_data['vacancies_processed'] = len(list(filter(lambda x: x, salaries)))
    lang_data['average_salary'] = calculate_average_salary(salaries)
    return lang_data


if __name__ == '__main__':
    result = {}
    for lang in languages:
        result[lang] = get_lang_data(lang)

    print(result)
