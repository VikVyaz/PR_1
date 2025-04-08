import datetime
import json
import os
import urllib.parse
import urllib.request
from typing import Any, Union

import finnhub
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


# ------------------------------------------------------Веб-страницы---------------------------------------------------
# ---------------------------------------------------Страница "Главная"------------------------------------------------


def to_open_file(path: str, true_list_or_false_df: bool = True) -> Any:
    """
    Функция открытия файла(JSON/CSV/XLSX опционально)
    * outgoing_type_list - флаг типа выходных данных:
        ** True - list
        ** False - pd.DataFrame

    * Если JSON файл содержит dict, а не list[dict] - вернет dict при любом true_list_or_false_df
    """

    df = pd.DataFrame()
    if ".json" in path:
        try:  # Не забыть, что try тут, чтоб можно быть прочесть json не только list[dict], но и dict
            df = pd.read_json(path)
        except ValueError:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                return data
    elif ".csv" in path:
        df = pd.read_csv(path, delimiter=";")
    elif ".xlsx" in path:
        df = pd.read_excel(path)

    if true_list_or_false_df:
        new_df = df.fillna("")
        result = new_df.to_dict("records")

        return result
    else:
        return df


def to_get_filtered_data(date: str, transactions: pd.DataFrame) -> pd.DataFrame:
    """Функция фильтрации транзакций по исходной дате
    date - str формата '%Y-%m-%d %H:%M:%S'
    """

    desired_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    beginning_of_the_month = datetime.datetime(desired_date.year, desired_date.month, 1, 0, 0, 0)

    tr_df = transactions.copy()
    tr_df['Дата операции'] = pd.to_datetime(tr_df['Дата операции'], format="%d.%m.%Y %H:%M:%S")
    tr_result = tr_df[
        (tr_df['Дата операции'] >= beginning_of_the_month) &
        (tr_df['Дата операции'] <= desired_date)
        ]

    return tr_result


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


def show_cards_info(filtered_data: pd.DataFrame) -> list:
    """Функция отображения данный по картам:
    1. 4 последних цифры карт,
    2. Общие траты,
    3. Кешбэк (1руб за каждые 100руб).
    date - формат 'YYYY-MM-DD HH:MM:SS'
    """

    grouped = filtered_data[filtered_data['Сумма операции'] < 0][['Номер карты', 'Сумма операции']].groupby(
        'Номер карты').sum().round(2)
    grouped['Сумма операции'] = grouped['Сумма операции'].apply(lambda x: abs(x))
    grouped['Кэшбек'] = grouped['Сумма операции'].apply(lambda x: round(x / 100, 1))
    grouped = grouped.reset_index()
    return grouped.to_dict('records')


def show_top_transactions(filtered_data: pd.DataFrame) -> list:
    """Функция вывода топ-5 транзакций по сумме платежа"""

    top_5 = filtered_data[filtered_data['Сумма операции'] < 0][
        ["Сумма операции", "Дата операции", "Номер карты", "Категория", "Описание"]]

    top_5 = top_5.dropna(subset=['Номер карты']).sort_values('Сумма операции')
    top_5['Дата операции'] = top_5['Дата операции'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return top_5.head().to_dict('records')


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


in_df = pd.DataFrame({
        "Сумма операции": [-5000, -4000, -3000, -2000, -1000],
        "Дата операции": [
            pd.Timestamp('2021-10-14 16:44:00'),
            pd.Timestamp('2021-10-14 16:44:00'),
            pd.Timestamp('2021-10-14 16:44:00'),
            pd.Timestamp('2021-10-14 16:44:00'),
            pd.Timestamp('2021-10-14 16:44:00')
        ],
        "Номер карты": ['1', '2', '3', '4', '5'],
        "Категория": ['1', '2', '3', '4', '5'],
        "Описание": ['1', '2', '3', '4', '5']
    })

in_date = "2021-10-20 16:44:00"
# filtered = to_get_filtered_data(in_date, in_data)
# print(filtered.to_dict('records'))
# print(show_cards_info(filtered))
print(show_top_transactions(in_df))
