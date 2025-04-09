import datetime
import logging
import os
import typing
from functools import wraps
from typing import Any, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

# from src.views import to_open_file


# -------------------------------------------------logging--------------------------------------------------------------
def to_log_decorator(file_name: str = "") -> Any:
    """
    Декоратор логирования отчетов.
    * file_name - имя файла для логов - по умолчанию 'default_log_file'
    Лог будет сохранен в папку logs
    """

    if not file_name:
        file_name = "default_log_file"

    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        filename=f"{log_dir}/{file_name}.log",
        filemode="a",
        encoding="utf-8",
        format="[%(asctime)s | %(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
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

def to_save_result(file_name: str = 'results', file_type: str = 'json') -> Any:
    """
    Декоратор, сохраняющий результирующий DataFrame(!!!) в файл

    :param file_name: str; имя файла без расширения
    :param file_type: str; расширение по умолчанию = json. Доступные расширения: 'json', 'csv', 'excel'(или 'xslx')
    :return:
    """

    def save_result(func):
        @wraps(func)
        def save_this(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if not isinstance(result, pd.DataFrame):
                    raise TypeError('Файл не сохранен. Ожидался DataFrame')

                data_path = os.path.join(os.getcwd(), 'data')
                os.makedirs(data_path, exist_ok=True)

                clean_type = file_type.lower()
                path = os.path.join(data_path, f'{file_name}.{clean_type}')

                if clean_type == 'json':
                    result.to_json(f'{path}', orient='records', lines=True, force_ascii=False)
                elif clean_type == 'csv':
                    result.to_csv(f'{path}', index=False,encoding='utf-8-sig')
                elif clean_type in ['excel', 'xlsx']:
                    result.to_excel(f'{path}', index=False, engine='openpyxl')
                else:
                    raise ValueError('Файл не сохранен. Доступные типы файла json, csv или excel(xlsx)')

                print('Файл успешно сохранен')
                return result

            except TypeError as te:
                print(f'{te}')
            except ValueError as ve:
                print(f'{ve}')
            except Exception as e:
                print(f'Неизвестная ошибка {e}')

        return save_this
    return save_result


# ______________________________________________________________________________________________________________________

@to_save_result('spending_by_category')
@to_save_result('spending_by_category', 'csv')
@to_save_result('spending_by_category', 'xlsx')
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция вычисления трат по заданной категории за последние 3 месяца от даты.

    * transactions - DataFrame с транзакциями
    * category - категория, по которой вычисляются траты
    * date - дата, от которой ведется исчисление трат за последние 3 месяца
        ** по умолчанию - сегодня; формат - "YYYY-MM-DD HH:MM:SS"
    """

    if not date:
        true_date = datetime.datetime.now().replace(microsecond=0)
    else:
        true_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    minus_3_months = true_date - relativedelta(months=3)

    datetime_df = transactions

    datetime_df["Дата операции"] = datetime_df["Дата операции"].apply(
        lambda x: datetime.datetime.strptime(x, "%d.%m.%Y %H:%M:%S")
    )

    filtered_by_date_df = datetime_df[
        (minus_3_months <= datetime_df["Дата операции"]) & (datetime_df["Дата операции"] <= true_date)
    ]

    filtered_df = filtered_by_date_df[["Категория", "Сумма операции"]]
    only_expenses = filtered_df[filtered_df['Сумма операции'] < 0]
    category_df = only_expenses.groupby("Категория", as_index=False)["Сумма операции"].sum()

    result = pd.DataFrame(category_df[category_df["Категория"] == category]).reset_index(drop=True)

    return result


# if __name__ == "__main__":
# path = '../draft/operations.json'
# path = '../data/operations.xlsx'
# from_data = to_open_file(path, False)
# x1 = spending_by_category(from_data, "3", '2021-12-30 16:23:23')
# print(x1)
# @to_save_result(file_type='xlsx')
# def df_return():
#     return pd.DataFrame(
#         {
#             "Дата операции": [
#                 "21.11.2021 16:44:00",
#                 "10.10.2021 16:44:00",
#                 "10.10.2021 16:44:00",
#                 "07.08.2021 16:44:00",
#             ],
#             "Сумма операции": [2, -3, 4, -4],
#             "Категория": ["2", "3", "3", "3"],
#         }
#     )
#
# df_return()
