import datetime
from collections import defaultdict
from typing import DefaultDict

from src.reports import to_log_decorator

# from src.views import to_open_file


@to_log_decorator()
def cashback_profit(data: list, year: int, month: int) -> dict:
    """Функция вычисления выгодной категории кэшбэка
    в зависимости от года и месяца"""

    filtered_data = to_filter_data(data, year, month)
    result = to_get_category(filtered_data)

    return result


def to_filter_data(data: list, year: int, month: int) -> list:
    """Функция фильтрации транзакций по месяцу и году"""

    filtered_data = list(
        filter(
            lambda x: datetime.datetime.strptime(x["Дата операции"], "%d.%m.%Y %H:%M:%S").year == year
            and datetime.datetime.strptime(x["Дата операции"], "%d.%m.%Y %H:%M:%S").month == month,
            data,
        )
    )

    return filtered_data


def to_get_category(data: list) -> dict:
    """Функция анализа профитности категорий кэшбэка"""

    result: DefaultDict[str, int] = defaultdict(int)
    for transaction in data:
        for key, value in transaction.items():
            if key == "Категория" and transaction["Кэшбэк"]:
                result[value] += transaction["Кэшбэк"]

    sorted_result = dict(sorted(dict(result).items(), key=lambda x: x[1], reverse=True))

    return sorted_result


# if __name__ == '__main__':
# from_data = to_open_file('../data/operations.xlsx')
# from_data = to_open_file('../draft/operations.json')
# from_year = 2021
# from_month = 9
# print(cashback_profit(from_data, from_year, from_month))
