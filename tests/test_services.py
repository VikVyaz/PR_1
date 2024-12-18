from unittest.mock import patch, MagicMock

from src.services import cashback_profit, to_filter_data, to_get_category


@patch('src.services.to_get_category')
@patch('src.services.to_filter_data')
def test_cashback_profit(mock_data: MagicMock, mock_category: list) -> None:
    """Тест для src.services.cashback()"""

    mock_data.return_value = "whatever"
    mock_category.return_value = 0

    assert cashback_profit([], 0, 0) == 0


def test_to_filter_data(fixt_cashback: list) -> None:
    """Тест для src.services.to_filter_data()"""

    assert to_filter_data(
        fixt_cashback[0],
        fixt_cashback[1],
        fixt_cashback[2]
    ) == [fixt_cashback[0][0]]


def test_to_get_category(
        fixt_cashback: list,
        fixt_expected_get_category: dict) -> None:
    """Тест для src.services.to_get_category()"""

    assert to_get_category(fixt_cashback[0]) == fixt_expected_get_category
