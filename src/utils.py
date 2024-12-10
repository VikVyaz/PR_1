from typing import Any
import json

import pandas as pd


def to_open_file(path: str, type_list_else_df: bool = True) -> Any:
    """
    Функция открытия файла(JSON/CSV/XLSX опционально)
    * outgoing_type_list - флаг типа выходных данных:
        ** True - list
        ** False - pd.DataFrame
    """

    df = pd.DataFrame()
    if '.json' in path:
        try:
            df = pd.read_json(path)
        except ValueError:
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
                return data
    elif '.csv' in path:
        df = pd.read_csv(path, delimiter=';')
    elif '.xlsx' in path:
        df = pd.read_excel(path)

    if type_list_else_df:
        df = df.astype('object')
        pd.set_option('future.no_silent_downcasting', True)
        df.fillna("", inplace=True)
        result = df.to_dict('records')

        for transaction in result:
            for key, value in transaction.items():
                if key == 'id' and value:
                    transaction[key] = int(value)

        return result
    else:
        return df
