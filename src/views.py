import datetime
import os
import urllib.parse
import urllib.request
from typing import Union

import finnhub
import requests
from dotenv import load_dotenv

from src.utils import to_open_file

load_dotenv()

main_page_data_path = "./data/operations.xlsx"
main_page_user_settings_path = "./user_settings.json"


def main_page(date: str) -> dict:
    """Функция для отображения данных на главной странице:
    1. Приветствие
    2. Информация о картах
    3. Топ-5 транзакция за данный период
    4. Курс валют
    5. Курс S&P500
    """

    data = to_open_file(main_page_data_path)
    user_settings = to_open_file(main_page_user_settings_path)
    filtered_data = to_get_filtered_data(date, data)
    result = {
        "greeting": greeting(),
        "cards": show_cards_info(filtered_data),
        "top_transactions": show_top_transactions(filtered_data),
        "currency_rate": show_currency_rates(dict(user_settings)),
        "stock_prices": show_stock_prices(dict(user_settings)),
    }

    return result


def to_get_filtered_data(date: str, transactions: list[dict]) -> list:
    """Функция фильтрации транзакций по исходной дате
    date - str формата '%Y-%m-%d %H:%M:%S'
    """

    desired_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    beginning_of_the_month = datetime.datetime(desired_date.year, desired_date.month, 1, 0, 0, 0)

    filtered_data = list(
        filter(
            lambda x: beginning_of_the_month
            <= datetime.datetime.strptime(x["Дата операции"], "%d.%m.%Y %H:%M:%S")
            <= desired_date,
            transactions,
        )
    )

    return filtered_data


def greeting() -> str:
    """Функция приветствия в зависимости от времени суток"""

    current_time = datetime.datetime.now().hour

    if 6 <= current_time < 12:
        current_greeting = "Доброе утро!"
    elif 12 <= current_time < 17:
        current_greeting = "Добрый день!"
    elif 17 <= current_time < 22:
        current_greeting = "Добрый вечер!"
    else:
        current_greeting = "Доброй ночи!"

    return current_greeting


def show_cards_info(filtered_data: list) -> list:
    """Функция отображения данный по картам:
    1. 4 последних цифры карт,
    2. Общие траты,
    3. Кешбэк (1руб за каждые 100руб).
    date - формат 'YYYY-MM-DD HH:MM:SS'
    """

    cards_number = []
    for tr in filtered_data:
        if tr["Номер карты"]:
            cards_number.append(tr["Номер карты"])
    cards_number = list(dict.fromkeys(cards_number))

    result = []

    for card_num in list(cards_number):
        card_dict = {}
        total_spent = 0
        card_dict["last_digits"] = card_num[-4:]
        for tr in filtered_data:
            if tr["Номер карты"] == card_num and tr["Сумма платежа"] < 0:
                total_spent += -tr["Сумма платежа"]
        card_dict["total_spent"] = round(total_spent, 2)
        card_dict["cashback"] = round((total_spent / 100 if total_spent >= 0 else 0), 2)
        result.append(card_dict)

    return result


def show_top_transactions(filtered_data: list[dict]) -> list:
    """Функция вывода топ-5 транзакций по сумме платежа"""

    top_transactions = sorted(filtered_data, key=lambda x: abs(x["Сумма платежа"]), reverse=True)

    top_5 = []
    top_5_tr = top_transactions[:5]
    for tr in top_5_tr:
        dict_for_tr = {
            "date": tr["Дата операции"][:10],
            "amount": tr["Сумма платежа"],
            "category": tr["Категория"],
            "description": tr["Описание"],
        }
        top_5.append(dict_for_tr)

    return top_5


def show_currency_rates(user_settings: dict) -> Union[list, str]:
    """Функция обработки и вывода курсов
    необходимых (согласно user_settings.json) валют"""

    apikey = os.getenv("EXCHANGE_APIKEY")

    url = "https://api.apilayer.com/fixer/latest"
    currencies = user_settings["user_currencies"]
    params = {"symbols": ",".join(currencies), "base": "RUB"}
    encoded_params = urllib.parse.urlencode(params)
    full_url = f"{url}?{encoded_params}"
    headers = {"apikey": f"{apikey}"}

    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        api_result = response.json()
        result = [{"currency": symbols, "rate": round(1 / price, 2)} for symbols, price in api_result["rates"].items()]
        return result
    except requests.exceptions.HTTPError:
        return "HTTP Error"
    except requests.exceptions.RequestException:
        return "Request Exception Error"


def show_stock_prices(user_settings: dict) -> Union[list, str]:
    """Функция обработки и вывода необходимых
    (согласно user_settings.json) котировок"""

    apikey = os.getenv("STOCK_APIKEY")
    client = finnhub.Client(api_key=apikey)

    stock_result = {}
    try:
        for stock_symbol in user_settings["user_stocks"]:
            price = client.quote(stock_symbol)["c"]
            stock_result[stock_symbol] = price

        result = [{"stock": symbol, "price": price} for symbol, price in stock_result.items()]
        return result
    except requests.exceptions.HTTPError:
        return "HTTP Error"
    except requests.exceptions.RequestException:
        return "Request Exception Error"


# if __name__ == '__main__':
# main_page_data_path = '../data/operations.xlsx'
# main_page_user_settings_path = '../user_settings.json'
# print(main_page('2021-10-30 15:23:22'))
