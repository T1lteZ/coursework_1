import json
import logging
import os
import urllib.request
from datetime import datetime, timedelta

import pandas as pd
import requests
from dotenv import load_dotenv

logger = logging.getLogger("utils.log")
file_handler = logging.FileHandler("logs/utils.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

load_dotenv()
API_KEY_VALUTE = os.getenv("API_KEY_VALUTE")

API_KEY_500 = os.getenv("API_KEY_500")


def reader_transaction_excel(file_path) -> pd.DataFrame:
    """Функция принимает на вход путь до файла и возвращает датафрейм"""
    logger.info(f"Вызвана функция получения транзакций из файла {file_path}")
    try:
        df_transactions = pd.read_excel(file_path)
        logger.info(f"Файл {file_path} найден, данные о транзакциях получены")

        return df_transactions
    except FileNotFoundError:
        logger.info(f"Файл {file_path} не найден")
        raise


def read_excel(path: str) -> list[dict]:
    """Функция принимает путь до xlsx файла и создает список словарей с транзакциями"""
    try:
        df = pd.read_excel(path)
        logger.info("файл перекодирован в список словарей")
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Возникла ошибка {e}")
        logger.error(f"Возникла ошибка {e}")
        return []


def filter_by_date(df_transactions: pd.DataFrame, input_date_str: str) -> pd.DataFrame:
    """Функция принимает список словарей с транзакциями и дату
    фильтрует транзакции с начала месяца, на который выпадает входящая дата по входящую дату."""
    input_date = datetime.strptime(input_date_str, "%d.%m.%Y")
    end_date = input_date + timedelta(days=1)
    start_date = datetime(input_date.year, input_date.month, 1)

    def parse_date(date_str: str) -> datetime:
        """Функция переводит дату из формата строки в формат datetime"""
        return datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")

    filtered_transaction = df_transactions.loc[
        (pd.to_datetime(df_transactions["Дата операции"], dayfirst=True) <= end_date)
        & (pd.to_datetime(df_transactions["Дата операции"], dayfirst=True) >= start_date)
    ]

    logger.info(f"Транзакции в списке отфильтрованы по датам от {start_date} до {end_date}")
    return filtered_transaction


def greetings():
    """Функция приветствия"""
    time_obj = datetime.now()
    if 6 <= time_obj.hour <= 12:
        return "Доброе утро"
    elif 13 <= time_obj.hour <= 18:
        return "Добрый день"
    elif 19 <= time_obj.hour <= 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_cards_data(df_transactions: pd.DataFrame) -> pd.DataFrame:
    """Функция создает словарь с ключоми номеров карт и в значения добавляет сумму трат и сумму кэшбека"""
    cards_dict = (
        df_transactions.loc[df_transactions["Сумма платежа"] < 0]
        .groupby(by="Номер карты")
        .agg("Сумма платежа")
        .sum()
        .to_dict()
    )
    logger.debug(f"Получен словарь расходов по картам: {cards_dict}")
    expenses_cards = []
    for card, expenses in cards_dict.items():
        expenses_cards.append(
            {"last_digits": card, "total spent": abs(expenses), "cashback": abs(round(expenses / 100, 2))}
        )
        logger.info(f"Добавлен расход по карте {card}: {abs(expenses)}")

    logger.info("Завершение выполнения функции get_expenses_cards")
    return expenses_cards


def get_top_5_transactions(df_transactions):
    """Функция вывода топ 5 транзакций по сумме платежа"""
    logger.info("Начало работы функции top_transaction")
    try:
        if df_transactions is []:
            return []
        else:
            top_transaction = df_transactions.sort_values(by="Сумма платежа", ascending=True).iloc[:5]
            logger.info("Получен топ 5 транзакций по сумме платежа")
            result_top_transaction = top_transaction.to_dict(orient="records")
            top_transaction_list = []
            for transaction in result_top_transaction:
                top_transaction_list.append(
                    {
                        "date": str(
                            (datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S"))
                            .date()
                            .strftime("%d.%m.%Y")
                        ).replace("-", "."),
                        "amount": transaction["Сумма платежа"],
                        "category": transaction["Категория"],
                        "description": transaction["Описание"],
                    }
                )
            logger.info("Сформирован список топ 5 транзакций")
        return top_transaction_list
    except AttributeError:
        return []


def currency_rates(currency: list, api_key) -> list[dict]:
    """Функция запроса курса валют"""
    logger.info("Начало работы функции (currency_rates)")
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


def get_price_stock(stocks: list, api_key) -> list:
    """Функция для получения данных об акциях из списка S&P500"""
    logger.info("Начало работы функции (get_price_stock)")
    logger.info("Функция обрабатывает данные транзакций.")
    for stock in stocks:
        logger.info("Перебор акций в списке 'stocks' в функции (get_price_stock)")
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&interval=60min&apikey={api_key}"
        response = requests.get(url)
        result = response.json()

    logger.info("Функция get_price_stock успешно завершила свою работу")
    return result
