import os
import urllib.parse
import urllib.request
import requests
import pandas as pd
import datetime
import json
from dotenv import load_dotenv
import finnhub
from typing import Union, Any

load_dotenv()


def main_page(date: str, original_data: str, original_user_settings: str) -> dict:
    """Main-функция для Веб-страницы/Страница 'Главная'
    """

    data = to_open_file(original_data)
    user_settings = to_open_file(original_user_settings)
    filtered_data = to_get_filtered_data(date, data)
    result = {
        'greeting': greeting(),
        'cards': show_cards_info(filtered_data),
        'top_transactions': show_top_transactions(filtered_data),
        'currency_rate': show_currency_rates(user_settings),
        'stock_prices': show_stock_prices(user_settings)
    }

    return result


def to_open_file(path: str) -> Union[list, dict]:
    """Функция открытия файла(JSON/CSV/XLSX опционально)"""

    df = pd.DataFrame()
    if '.json' in path:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        return data
    elif '.csv' in path:
        df = pd.read_csv(path, delimiter=';')
    elif '.xlsx' in path:
        df = pd.read_excel(path)

    df = df.astype('object')
    pd.set_option('future.no_silent_downcasting', True)
    df.fillna("", inplace=True)
    result = df.to_dict('records')

    for transaction in result:
        for key, value in transaction.items():
            if key == 'id' and value:
                transaction[key] = int(value)

    return result


def to_get_filtered_data(date: str, transactions: list[dict]) -> list:
    """Функция фильтрации транзакций по исходной дате
    date - str формата '%Y-%m-%d %H:%M:%S'
    """

    desired_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    beginning_of_the_month = datetime.datetime(
        desired_date.year,
        desired_date.month,
        1, 0, 0, 0
    )

    filtered_data = list(filter(
        lambda x: beginning_of_the_month <= datetime.datetime.strptime(x['Дата операции'],
                                                                       '%d.%m.%Y %H:%M:%S') <= desired_date,
        transactions))

    return filtered_data


def greeting() -> str:
    """Функция приветствия в зависимости от времени суток"""

    current_time = datetime.datetime.now().hour

    if 6 <= current_time < 12:
        current_greeting = 'Доброе утро!'
    elif 12 <= current_time < 18:
        current_greeting = 'Добрый день!'
    else:
        current_greeting = 'Доброй ночи!'

    return current_greeting


def show_cards_info(filtered_data: list[dict]) -> list:
    """Функция отображения данный по картам:
    1. 4 последних цифры карт,
    2. Общие траты,
    3. Кешбэк (1руб за каждые 100руб).
    date - формат 'YYYY-MM-DD HH:MM:SS'
    """

    cards_number = set()
    for tr in filtered_data:
        if tr['Номер карты']:
            cards_number.add(tr['Номер карты'])

    result = []

    for card_num in list(cards_number):
        card_dict = {}
        total_spent = 0
        card_dict['last_digits'] = card_num[-4:]
        for tr in filtered_data:
            if tr['Номер карты'] == card_num:
                total_spent -= tr['Сумма платежа']
        card_dict['total_spent'] = round(total_spent, 2)
        card_dict['cashback'] = round((total_spent / 100 if total_spent >= 0 else 0), 2)
        result.append(card_dict)

    return result


def show_top_transactions(filtered_data: list[dict]) -> list:
    """Функция вывода топ-5 транзакций по сумме платежа"""

    top_transactions = sorted(filtered_data, key=lambda x: abs(x['Сумма платежа']), reverse=True)

    top_5 = []
    top_5_tr = top_transactions[:5]
    for tr in top_5_tr:
        dict_for_tr = {'date': tr['Дата операции'][:10],
                       'amount': tr['Сумма платежа'],
                       'category': tr['Категория'],
                       'description': tr['Описание']
                       }
        top_5.append(dict_for_tr)

    return top_5


def show_currency_rates(user_settings: dict) -> Union[list, None]:
    """Функция обработки и вывода курсов
    необходимых (согласно user_settings.json) валют"""

    apikey = os.getenv('EXCHANGE_APIKEY')

    url = "https://api.apilayer.com/fixer/latest"
    currencies = user_settings["user_currencies"]
    params = {
        "symbols": ",".join(currencies),
        "base": "RUB"
    }
    encoded_params = urllib.parse.urlencode(params)
    full_url = f"{url}?{encoded_params}"
    headers = {
        "apikey": f"{apikey}"
    }

    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        api_result = response.json()
        result = [
            {"currency": symbols, "rate": round(1 / price, 2)}
            for symbols, price in api_result["rates"].items()
        ]
        return result
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e.response.status_code} - {e.response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")


def show_stock_prices(user_settings: dict) -> list:
    """Функция обработки и вывода необходимых
    (согласно user_settings.json) котировок"""

    apikey = os.getenv("STOCK_APIKEY")
    client = finnhub.Client(api_key=apikey)

    stock_result = {}
    for stock_symbol in user_settings["user_stocks"]:
        price = client.quote(stock_symbol)["c"]
        stock_result[stock_symbol] = price

    result = [
        {"stock": symbol, "price": price}
        for symbol, price in stock_result.items()
    ]
    return result


if __name__ == '__main__':
    from_data = '../data/operations.xlsx'
    from_user_settings = '../user_settings.json'
    print(main_page('2021-10-30 15:23:22', from_data, from_user_settings))
