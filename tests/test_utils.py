from unittest.mock import MagicMock, Mock, mock_open, patch

import pandas as pd

from src.utils import to_open_file

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
@patch("src.utils.pd.read_json")
def test_to_open_file_json_failure(mock_json_err: MagicMock, mock_load: MagicMock, mock_open_file: MagicMock) -> None:
    """Тест для src.utils.to_open_file() когда JSON состоит из dict, а не list[dict]"""

    mock_json_err.side_effect = ValueError
    mock_load.return_value = expected_list

    assert to_open_file(input_paths[0]) == expected_list
