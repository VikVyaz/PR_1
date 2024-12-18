from src.reports import spending_by_category
from src.services import cashback_profit
from src.utils import to_open_file
from src.views import main_page

if __name__ == "__main__":
    # ------------------------------------Веб-страницы-----------------------------------
    # ------------------------------------views.py---------------------------------------
    main_page_date = '2021-10-30 15:23:22'

    # 1. Страница "Главная"
    print(main_page(main_page_date))

    # ------------------------------------Сервисы------------------------------------
    # -----------------------------------services.py---------------------------------
    input_path = './data/operations.xlsx'
    from_data = to_open_file(input_path)
    from_year = "2021"
    from_month = "10"

    # 1. Выгодные категории повышенного кэшбека
    print(cashback_profit(from_data, int(from_year), int(from_month)))

    # --------------------------------Отчеты------------------------------------
    path = './data/operations.xlsx'
    from_data = to_open_file(path, False)
    category = "Каршеринг"

    # 1. Траты по категориям
    print(spending_by_category(from_data, category, "2021-10-06 18:43:36"))
