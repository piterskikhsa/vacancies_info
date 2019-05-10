import requests


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


def get_predict_rub_salary_hh(vacancy):
    salary = vacancy['salary']
    if not salary or not is_salary_rub(salary, 'RUR'):
        return None
    return get_predict_salary(salary['from'], salary['to'])


def get_predict_rub_salary_sj(vacancy):
    if not is_salary_rub(vacancy, 'rub'):
        return None
    return get_predict_salary(vacancy['payment_from'], vacancy['payment_to'])


def main():
    pass


if __name__ == '__main__':
    main()