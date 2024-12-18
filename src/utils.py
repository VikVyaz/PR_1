import json
from typing import Any

import pandas as pd


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
