import pandas as pd
import pytest

# ------------------------------------Веб-страницы-----------------------------------
# ------------------------------------views.py---------------------------------------


@pytest.fixture()
def fixt_in_out_filtered_data() -> list:
    """"""

    in_data = [
        {"Дата операции": "14.10.2021 16:44:00"},
        {"Дата операции": "14.02.2021 16:44:00"},
        {"Дата операции": "11.10.2021 16:44:00"},
    ]

    in_date = "2021-10-20 16:44:00"

    out_data = [{"Дата операции": "14.10.2021 16:44:00"}, {"Дата операции": "11.10.2021 16:44:00"}]

    return [in_date, in_data, out_data]


@pytest.fixture()
def fixt_transactions() -> list:
    in_data = [
        {
            "Дата операции": "11.10.2021 16:44:00",
            "Номер карты": "*1234",
            "Сумма платежа": -400,
            "Категория": "1",
            "Описание": "1",
        },
        {
            "Дата операции": "11.10.2021 16:44:00",
            "Номер карты": "*1234",
            "Сумма платежа": -300,
            "Категория": "2",
            "Описание": "2",
        },
        {
            "Дата операции": "11.10.2021 16:44:00",
            "Номер карты": "*5678",
            "Сумма платежа": -200,
            "Категория": "3",
            "Описание": "3",
        },
        {
            "Дата операции": "11.10.2021 16:44:00",
            "Номер карты": "*5678",
            "Сумма платежа": -100,
            "Категория": "4",
            "Описание": "4",
        },
    ]

    return in_data


@pytest.fixture()
def fixt_show_cards_info_out() -> list:
    out_card_data = [
        {"last_digits": "1234", "total_spent": 700, "cashback": 7.0},
        {"last_digits": "5678", "total_spent": 300, "cashback": 3.0},
    ]

    return out_card_data


@pytest.fixture()
def fixt_show_top_transactions_out() -> list:
    return [
        {"date": "11.10.2021", "amount": -400, "category": "1", "description": "1"},
        {"date": "11.10.2021", "amount": -300, "category": "2", "description": "2"},
        {"date": "11.10.2021", "amount": -200, "category": "3", "description": "3"},
        {"date": "11.10.2021", "amount": -100, "category": "4", "description": "4"},
    ]


@pytest.fixture()
def fixt_currency_rates() -> list:
    api_out_data = {"rates": {"test1": 2, "test2": 4}}

    out_data = [{"currency": "test1", "rate": 0.5}, {"currency": "test2", "rate": 0.25}]

    return [api_out_data, out_data]


# ------------------------------------Сервисы------------------------------------
# -----------------------------------services.py---------------------------------
@pytest.fixture()
def fixt_cashback() -> list:
    data_input = [
        {"Дата операции": "01.09.2021 16:44:00", "Кэшбэк": 30, "Категория": "Three"},
        {"Дата операции": "01.12.2021 16:42:04", "Кэшбэк": 20, "Категория": "Two"},
        {"Дата операции": "01.12.2022 16:39:04", "Кэшбэк": 10, "Категория": "One"},
    ]
    year = 2021
    month = 9

    return [data_input, year, month]


@pytest.fixture()
def fixt_expected_get_category() -> dict:
    data_output = {"Three": 30, "Two": 20, "One": 10}

    return data_output


# -------------------------------------Отчеты-----------------------------------
# -----------------------------------reports.py---------------------------------
@pytest.fixture()
def fixt_spending_by_category() -> list:
    """"""

    input_df = pd.DataFrame(
        {
            "Дата операции": [
                "21.11.2021 16:44:00",
                "10.10.2021 16:44:00",
                "10.10.2021 16:44:00",
                "07.08.2021 16:44:00",
            ],
            "Сумма операции": [-2, 3, -4, 4],
            "Категория": ["2", "3", "3", "3"],
        }
    )

    expected_df = pd.DataFrame({"Категория": ["3"], "Сумма операции": [-1]})

    return [input_df, expected_df]


# -----------------------------------utils.py---------------------------------
@pytest.fixture()
def fixt_to_open_file() -> list:
    """"""

    dict_for_df = {"A": [1, 2, 3], "B": [4, 5, 6]}
    test_df = pd.DataFrame(dict_for_df)
    expected_list = [{"A": 1, "B": 4}, {"A": 2, "B": 5}, {"A": 3, "B": 6}]
    return [test_df, expected_list]
