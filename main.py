import datetime as dt
import json as js
import os

import exceptions
import requests
from dotenv import load_dotenv

load_dotenv()

MY_PHONE = os.getenv('MY_PHONE')
DB_TD = os.getenv('DB_TD')
DB_LOGIN = os.getenv('DB_LOGIN')
DB_PWD = os.getenv('DB_PWD')

TODAY = dt.datetime.now()
POST_ENDPOINT = 'http://sirius.abr95.ru/api/token/v1/5bca212e899b0da01dd6a6675f5cd50c/'
DB_ENDPOINT = 'http://test-server.abs95.ru/api/admin/v1/lic/readfile'

token_dict = {
    'MY_PHONE': MY_PHONE,
    'DB_TD': DB_TD,
    'DB_LOGIN': DB_LOGIN,
    'DB_PWD': DB_PWD,
}


def get_api_answer(url):
    """Отправляем запрос на эндпоинт API с базой данных."""
    params = {
        'td': DB_TD,
        'login': DB_LOGIN,
        'pwd': DB_PWD
    }
    request = requests.get(url, params=params)
    if request.status_code != 200:
        raise exceptions.EndPointIsNotAvailiable(request.status_code)
    return request.json()


def check_tokens():
    """Проверка наличия всех нужных токенов"""
    if all((MY_PHONE, DB_TD, DB_LOGIN, DB_PWD)):
        return bool


def get_date(request):
    """Получаем дату из json и конверктируем её."""
    data = js.loads(request.text)
    dtstop = data['data']['configurations'][0]['smart']['dtstop']
    dtstop = dt.datetime.strptime(dtstop, '%Y-%m-%d %H:%M:%S')
    return dtstop


def post(raz_days: int):
    """Отправляем на эндпоинт запрос с необходимыми
    данными для обработки на стороне API."""
    if raz_days < 7:
        json = {"days": raz_days, "alarm": "true", "phone": MY_PHONE}
        request = requests.post(POST_ENDPOINT, json=json)
        if request.status_code != 201:
            raise exceptions.EndPointIsNotAvailiable(request.status_code)
        print(request.status_code)
    elif raz_days > 7:
        json = {"days": raz_days, "alarm": "false", "phone": MY_PHONE}
        request = requests.post(POST_ENDPOINT, json=json)
        if request.status_code != 201:
            raise exceptions.EndPointIsNotAvailiable(request.status_code)
        print(request.status_code)


def main():
    """Основная логика программы"""
    if not check_tokens():
        for key, token in token_dict.items():
            if not token:
                message = f'Токен {key} потерялся'
                print(message)
                raise exceptions.TokenNotFoundException(message)

    try:
        request = get_api_answer(DB_ENDPOINT)
        raz_date = get_date(request) - TODAY
        post(raz_date.days)
    except exceptions.EndPointIsNotAvailiable as error:
        message = f'Один из эндпоинтов недоступен, ошибка: {error}'
        print(message)
    except Exception as error:
        message = f'При работе программы произошла ошибка: {error}'
        print(message)


if __name__ == '__main__':
    main()
