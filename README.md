# Сравниваем вакансии программистов

Скрипт предназначен для поиска вакансий и получения средней заработной платы по вакансии.
Для сравнения выводятся вакансии с 2х сервисов: HeadHunter и SuperJob

## Как установить

### Скачать исходный код

- командой `$ git clone https://github.com/piterskikhsa/vacancies_info`
 

### Скачать зависимости

Убедитесь, что вы находитесь в папке с проектом:

```
$ cd vacancies_info
```
Скачать и установить зависимости:

```
pipenv install
```

Активировать созданное виртуальное окружение:
```
pipenv shell
```

### Запустить

Перед запуском убедитесь, что вы зарегистрировались на сайте SuperJob  и добавили в переменные окружения полученный токен.
Например в файл .env:

```
...
SUPERJOB_TOKEN=v3.r.1236 ....
```

Можем запускать:

```
python vacancies_info.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).