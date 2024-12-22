from src.reports import to_log_decorator
from src.utils import (
    greeting,
    show_cards_info,
    show_currency_rates,
    show_stock_prices,
    show_top_transactions,
    to_get_filtered_data,
    to_open_file,
)

main_page_data_path = "./data/operations.xlsx"
main_page_user_settings_path = "./user_settings.json"


@to_log_decorator()
def main_page(date: str) -> dict:
    """Функция для отображения данных на главной странице:
    1. Приветствие
    2. Информация о картах
    3. Топ-5 транзакция за данный период
    4. Курс валют
    5. Курс S&P500
    """

    data = to_open_file(main_page_data_path)
    user_settings = to_open_file(main_page_user_settings_path)
    filtered_data = to_get_filtered_data(date, data)
    result = {
        "greeting": greeting(),
        "cards": show_cards_info(filtered_data),
        "top_transactions": show_top_transactions(filtered_data),
        "currency_rate": show_currency_rates(dict(user_settings)),
        "stock_prices": show_stock_prices(dict(user_settings)),
    }

    return result


# if __name__ == '__main__':
#     main_page_data_path = '../data/operations.xlsx'
#     main_page_user_settings_path = '../user_settings.json'
#     print(main_page('2021-10-30 15:23:22'))
