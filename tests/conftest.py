import pytest


# ------------------------------------views.py---------------------------------------


@pytest.fixture()
def fixt_in_out_filtered_data() -> list:
    """"""

    in_data = [
        {"Дата операции": "14.10.2021 16:44:00"},
        {"Дата операции": "14.02.2021 16:44:00"},
        {"Дата операции": "11.10.2021 16:44:00"}
    ]

    in_date = "2021-10-20 16:44:00"

    out_data = [
        {"Дата операции": "14.10.2021 16:44:00"},
        {"Дата операции": "11.10.2021 16:44:00"}
    ]

    return [in_date, in_data, out_data]


@pytest.fixture()
def fixt_transactions() -> list:
    in_data = [
        {'Дата операции': '11.10.2021 16:44:00', 'Номер карты': "*1234", 'Сумма платежа': -400, 'Категория': '1',
         'Описание': '1'},
        {'Дата операции': '11.10.2021 16:44:00', 'Номер карты': "*1234", 'Сумма платежа': -300, 'Категория': '2',
         'Описание': '2'},
        {'Дата операции': '11.10.2021 16:44:00', 'Номер карты': "*5678", 'Сумма платежа': -200, 'Категория': '3',
         'Описание': '3'},
        {'Дата операции': '11.10.2021 16:44:00', 'Номер карты': "*5678", 'Сумма платежа': -100, 'Категория': '4',
         'Описание': '4'}
    ]

    return in_data


@pytest.fixture()
def fixt_show_cards_info_out() -> list:
    out_card_data = [
        {'last_digits': "1234", 'total_spent': 700, 'cashback': 7.0},
        {'last_digits': "5678", 'total_spent': 300, 'cashback': 3.0}
    ]

    return out_card_data


@pytest.fixture()
def fixt_show_top_transactions_out() -> list:
    return [
        {'date': '11.10.2021', 'amount': -400, 'category': '1', 'description': '1'},
        {'date': '11.10.2021', 'amount': -300, 'category': '2', 'description': '2'},
        {'date': '11.10.2021', 'amount': -200, 'category': '3', 'description': '3'},
        {'date': '11.10.2021', 'amount': -100, 'category': '4', 'description': '4'}
    ]


@pytest.fixture()
def fixt_currency_rates() -> list:
    api_out_data = {
        "rates": {
            "test1": 2,
            "test2": 4
        }
    }

    out_data = [
        {'currency': 'test1', 'rate': 0.5},
        {'currency': 'test2', 'rate': 0.25}
    ]

    return [api_out_data, out_data]
