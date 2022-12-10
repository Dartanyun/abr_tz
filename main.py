import requests
import json as js
import datetime as dt


def request(url: str) -> int:
    r = requests.get(url)
    today = dt.datetime.now()
    raz_date = get_date(r) - today
    raz_date = raz_date.days
    post(raz_date)


def get_date(r):
    """Получаем дату из json и конверктируем её."""
    data = js.loads(r.text)
    dtstop = data['data']['configurations'][0]['smart']['dtstop']
    dtstop = dt.datetime.strptime(dtstop, '%Y-%m-%d %H:%M:%S')
    return dtstop


def post(raz_days: int):
    MY_PHONE: int = 88005553535
    URL: str = 'http://sirius.abr95.ru/api/token/v1/5bca212e899b0da01dd6a6675f5cd50c'
    if raz_days < 7:
        value = {"days": raz_days, "alarm": "true", "phone": MY_PHONE}
        post = requests.post(URL, json=value)
        print(post.status_code)
    elif raz_days > 7:
        value = {"days": raz_days, "alarm": "false", "phone": MY_PHONE}
        post = requests.post(URL, json=value)
        print(post.status_code)


def main():
    request('http://test-server.abs95.ru/api/admin/v1/lic/readfile?td=abr.studio&login=student&pwd=123!StudeNT_321')


main()
