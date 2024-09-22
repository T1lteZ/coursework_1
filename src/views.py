import datetime
import json
import logging
import os
import urllib.request
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY_VALUTE = os.getenv("API_KEY_VALUTE")

API_KEY_500 = os.getenv("API_KEY_500")

logger = logging.getLogger("views.log")
file_handler = logging.FileHandler("views.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def filter_by_date(date: str, my_list: list) -> list:
    """Функция фильтрующая данные по заданной дате"""
    list_by_date = []
    logger.info("Начало работы функции (filter_by_date)")
    if date == "":
        return list_by_date
    year, month, day = int(date[0:4]), int(date[5:7]), int(date[8:10])
    date_obj = datetime.datetime(year, month, day)
    for i in my_list:
        if i["Дата платежа"] == "nan" or type(i["Дата платежа"]) is float:
            continue
        elif (
                date_obj
                >= datetime.datetime.strptime(str(i["Дата платежа"]), "%d.%m.%Y")
                >= date_obj - datetime.timedelta(days=day - 1)
        ):
            list_by_date.append(i)
    logger.info("Конец работы функции (filter_by_date)")
    return list_by_date


def currency_rates(currency: list) -> list[dict]:
    """Функция запроса курса валют"""
    logger.info("Начало работы функции (currency_rates)")
    api_key = API_KEY_VALUTE
    result = []
    for i in currency:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{i}"
        with urllib.request.urlopen(url) as response:
            body_json = response.read()
        body_dict = json.loads(body_json)
        result.append({"currency": i, "rate": round(body_dict["conversion_rates"]["RUB"], 2)})

    logger.info("Создание списка словарей для функции - currency_rates")

    logger.info("Окончание работы функции - currency_rates")
    return result


def get_price_stock(stocks: list) -> list:
    """Функция для получения данных об акциях из списка S&P500"""
    logger.info("Начало работы функции (get_price_stock)")
    api_key = API_KEY_500
    stock_prices = []
    logger.info("Функция обрабатывает данные транзакций.")
    for stock in stocks:
        logger.info("Перебор акций в списке 'stocks' в функции (get_price_stock)")
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
        response = requests.get(url, timeout=5, allow_redirects=False)
        result = response.json()

        stock_prices.append({"stock": stock, "price": round(float(result["Global Quote"]["05. price"]), 2)})
    logger.info("Функция get_price_stock успешно завершила свою работу")
    return stock_prices
