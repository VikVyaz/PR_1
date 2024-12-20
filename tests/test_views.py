import datetime
from unittest.mock import MagicMock, Mock, mock_open, patch

import pandas as pd
import pytest
import requests

from src.views import (greeting, show_cards_info, show_currency_rates, show_stock_prices, show_top_transactions,
                       to_get_filtered_data, to_open_file)

expected_list = [{"A": 1, "B": 4}, {"A": 2, "B": 5}, {"A": 3, "B": 6}]

input_paths = [".json", ".csv", ".xlsx"]


def test_to_open_file_df() -> None:
    """Тест для src.utils.to_open_file() с возвратом DataFrame"""

    mock_df = Mock(return_value="123")
    pd.read_json = mock_df
    pd.read_excel = mock_df
    pd.read_csv = mock_df

    for path in input_paths:
        assert to_open_file(path, False) == "123"


def test_to_open_file_list(fixt_to_open_file: list) -> None:
    """Тест для src.utils.to_open_file() с возвратом list[dict]/dict"""

    mock_df = Mock(return_value=fixt_to_open_file[0])
    pd.read_json = mock_df
    pd.read_excel = mock_df
    pd.read_csv = mock_df

    for path in input_paths:
        assert to_open_file(path) == fixt_to_open_file[1]


@patch("builtins.open", new_callable=mock_open)
@patch("json.load")
@patch("src.views.pd.read_json")
def test_to_open_file_json_failure(mock_json_err: MagicMock, mock_load: MagicMock, mock_open_file: MagicMock) -> None:
    """Тест для src.utils.to_open_file() когда JSON состоит из dict, а не list[dict]"""

    mock_json_err.side_effect = ValueError
    mock_load.return_value = expected_list

    assert to_open_file(input_paths[0]) == expected_list


def test_to_get_filtered_data(fixt_in_out_filtered_data: list) -> None:
    """Тест для to_get_filtered_data()"""

    assert (
        to_get_filtered_data(fixt_in_out_filtered_data[0], fixt_in_out_filtered_data[1])
        == fixt_in_out_filtered_data[2]
    )


greeting_test = [
    datetime.datetime(2020, 9, 13, 7),
    datetime.datetime(2020, 9, 13, 13),
    datetime.datetime(2020, 9, 13, 19),
    datetime.datetime(2020, 9, 13, 23),
]


@patch("src.views.datetime.datetime")
@pytest.mark.parametrize(
    "hour, response",
    [
        (greeting_test[0], "Доброе утро!"),
        (greeting_test[1], "Добрый день!"),
        (greeting_test[2], "Добрый вечер!"),
        (greeting_test[3], "Доброй ночи!"),
    ],
)
def test_greeting(mock_datetime: MagicMock, hour: list, response: str) -> None:
    """Тест для src.views.greeting()"""

    mock_datetime.now.return_value = hour
    assert greeting() == response


def test_show_cards_info(fixt_transactions: list, fixt_show_cards_info_out: list) -> None:
    """Тест для src.views.show_card_info()"""

    assert show_cards_info(fixt_transactions) == fixt_show_cards_info_out


def test_show_top_transactions(fixt_transactions: list, fixt_show_top_transactions_out: list) -> None:
    """Тест для src.views.show_top_transactions()"""

    assert show_top_transactions(fixt_transactions) == fixt_show_top_transactions_out


@patch("src.views.requests.get")
def test_show_currency_rates(mock_get: MagicMock, fixt_currency_rates: list) -> None:
    """Тест для src.views.show_currency_rates()"""

    mock_get.return_value.json.return_value = fixt_currency_rates[0]
    assert show_currency_rates({"user_currencies": "qwerty"}) == fixt_currency_rates[1]


@patch("src.views.requests.get")
def test_show_currency_rates_errors(mock_get: MagicMock, fixt_currency_rates: list) -> None:
    """Тест для обработки ошибок в src.views.show_currency_rates"""

    mock_get.side_effect = requests.exceptions.HTTPError
    assert show_currency_rates({"user_currencies": "qwerty"}) == "HTTP Error"

    mock_get.side_effect = requests.exceptions.RequestException
    assert show_currency_rates({"user_currencies": "qwerty"}) == "Request Exception Error"


user_settings_in = {"user_stocks": ["AAPL", "AMZN"]}

expected_result = [{"stock": "AAPL", "price": 1.0}, {"stock": "AMZN", "price": 1.0}]


@patch("src.views.finnhub.Client")
@patch("src.views.os.getenv")
def test_show_stock_prices(mock_getenv: MagicMock, mock_client: MagicMock):
    """Тест для src.views.show_stock_prices()"""

    mock_getenv.return_value = "fake_key"

    mock_quote = MagicMock()
    mock_quote.quote.return_value = {"c": 1.0}
    mock_client.return_value = mock_quote

    assert show_stock_prices(user_settings_in) == expected_result


@patch("src.views.finnhub.Client")
@patch("src.views.os.getenv")
def test_show_stock_prices_errors(mock_getenv: MagicMock, mock_client: MagicMock):
    """Тест для обработки ошибок в src.views.show_stock_prices()"""

    mock_getenv.return_value = "fake_key"

    mock_quote = MagicMock()
    mock_quote.quote.side_effect = requests.exceptions.HTTPError
    mock_client.return_value = mock_quote
    assert show_stock_prices(user_settings_in) == "HTTP Error"

    mock_quote = MagicMock()
    mock_quote.quote.side_effect = requests.exceptions.RequestException
    mock_client.return_value = mock_quote
    assert show_stock_prices(user_settings_in) == "Request Exception Error"
