import json
import logging

from src.utils import greetings, read_excel
from src.views import currency_rates, filter_by_date, get_price_stock

logger = logging.getLogger("utils.log")
file_handler = logging.FileHandler("main.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

data_frame = read_excel("../data/operations.xlsx")


def main(date: str, df_transactions, stocks: list, currency: list):
    """Функция создающая JSON ответ для страницы главная"""
    logger.info("Начало работы главной функции (main)")
    final_list = filter_by_date(date, df_transactions)
    greeting = greetings()
    stocks_prices = get_price_stock(stocks)
    currency_r = currency_rates(currency)
    logger.info("Создание JSON ответа")
    result = [{
            "greeting": greeting,
            "currency_rates": currency_r,
            "stock_prices": stocks_prices,
        }]
    date_json = json.dumps(
        result,
        indent=4,
        ensure_ascii=False,
    )
    logger.info("Завершение работы главной функции (main)")
    return date_json
