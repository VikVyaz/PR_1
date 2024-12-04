import json
from typing import Any

import pandas as pd


def to_open_file(path: str) -> Any:
    """Функция открытия файла(JSON/CSV/XLSX опционально)"""

    df = pd.DataFrame()
    if '.json' in path:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        return data
    elif '.csv' in path:
        df = pd.read_csv(path, delimiter=';')
    elif '.xlsx' in path:
        df = pd.read_excel(path)

    df = df.astype('object')
    pd.set_option('future.no_silent_downcasting', True)
    df.fillna("", inplace=True)
    result = df.to_dict('records')

    for transaction in result:
        for key, value in transaction.items():
            if key == 'id' and value:
                transaction[key] = int(value)

    return result
