from src.reports import to_log_decorator, spending_by_category
from unittest.mock import patch
import pandas as pd
import logging
import datetime
import pytest


def test_to_log_decorator() -> None:
    """Тест логирования src.reports.to_log_decorator"""

    @to_log_decorator()
    def test_func(a, b):
        return a + b

    with patch('logging.info') as mock_log_info:

        assert test_func(1, 1) == 2

        mock_log_info.assert_any_call("Function 'test_func', status: OK. Result: 2")

        assert mock_log_info.call_count == 1


def test_spending_by_category(fixt_spending_by_category: list) -> None:
    """Тест для src.reports.spending_by_category"""

    result = spending_by_category(fixt_spending_by_category[0], "3", '2021-12-30 16:23:23')
    expected_result = fixt_spending_by_category[1]

    assert result.to_dict('records') == expected_result.to_dict('records')
