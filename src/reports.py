import datetime
import logging
import os
import typing
from functools import wraps
from typing import Any, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.utils import to_open_file


# -------------------------------------------------logging--------------------------------------------------------------
def to_log_decorator(file_name: str = "") -> Any:
    """
    Декоратор логирования отчетов.
    * file_name - имя файла для логов - по умолчанию 'default_log_file'
    Лог будет сохранен в папку logs
    """

    if not file_name:
        file_name = "default_log_file"

    log_dir = "../logs"
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(level=logging.INFO,
                        filename=f"{log_dir}/{file_name}.log",
                        filemode="w",
                        encoding='utf-8',
                        format="[%(asctime)s | %(levelname)s]: %(message)s",
                        datefmt='%Y-%m-%d %H:%M:%S'
                        )

    def log_decor(func: typing.Any) -> typing.Any:
        @wraps(func)
        def log_this(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            try:
                logging.info(f"Function '{func.__name__}', status: OK. Result: {func(*args, **kwargs)}")
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(f"Function {func.__name__} crash down. Reason: {e}")
                raise Exception(f"Error: {e}")

        return log_this

    return log_decor
# ______________________________________________________________________________________________________________________


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция вычисления трат по заданной категории за последние 3 месяца от даты.

    * transactions - DataFrame с транзакциями
    * category - категория, по которой вычисляются траты
    * date - дата, от которой ведется исчисления периода трат
        ** по умолчанию - сегодня; формат - "YYYY-MM-DD HH:MM:SS"
    """

    if not date:
        true_date = datetime.datetime.now().replace(microsecond=0)
    else:
        true_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    minus_3_months = true_date - relativedelta(months=3)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)

    filtered_by_date_df = transactions[
        (minus_3_months <= transactions["Дата операции"])
        & (transactions["Дата операции"] <= date)
    ]

    filtered_df = filtered_by_date_df[["Категория", "Сумма операции"]]

    category_df = filtered_df.groupby("Категория")["Сумма операции"].sum().apply(lambda x: -x)
    category_df = category_df[category_df > 0]

    result = round(category_df[category], 2)

    return result


# if __name__ == "__main__":
    # path = '../data/operations.xlsx'
    # from_data = to_open_file(path, False)
    # x1 = spending_by_category(from_data, "Каршеринг", "2021-10-06 18:43:36")
    # print(x1)
