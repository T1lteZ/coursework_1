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


def filter_by_date(transactions: list[dict], input_date_str: str) -> list[dict]:
    """Функция принимает список словарей с транзакциями и дату
    фильтрует транзакции с начала месяца, на который выпадает входящая дата по входящую дату."""
    input_date = datetime.strptime(input_date_str, "%d.%m.%Y")
    end_date = input_date + timedelta(days=1)
    start_date = datetime(end_date.year, end_date.month, 1)

    def parse_date(date_str: str) -> datetime:
        """Функция переводит дату из формата строки в формат datetime"""
        return datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")

    filtered_transactions = [
        transaction
        for transaction in transactions
        if start_date <= parse_date(transaction["Дата операции"]) <= end_date
    ]
    logger.info(f"Транзакции в списке отфильтрованы по датам от {start_date} до {end_date}")
    return filtered_transactions


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


def get_cards_data(transactions: list[dict]) -> list[dict]:
    """Функция создает словарь с ключоми номеров карт и в значения добавляет сумму трат и сумму кэшбека"""
    card_data = {}
    for transaction in transactions:
        card_number = transaction.get("Номер карты")
        if not card_number or str(card_number).strip().lower() == "nan":
            continue
        amount = float(transaction["Сумма операции"])
        if card_number not in card_data:
            card_data[card_number] = {"total_spent": 0.0, "cashback": 0.0}
        if amount < 0:
            card_data[card_number]["total_spent"] += abs(amount)
            cashback_value = transaction.get("Кэшбэк")
            if transaction["Категория"] != "Переводы" and transaction["Категория"] != "Наличные":
                if cashback_value is not None:
                    cashback_amount = float(cashback_value)
                    if cashback_amount >= 0:
                        card_data[card_number]["cashback"] += cashback_amount
                    else:
                        card_data[card_number]["cashback"] += amount * -0.01
                else:
                    card_data[card_number]["cashback"] += amount * -0.01
    logger.info("кэшбек и суммы по картам посчитаны")
    cards_data = []
    for last_digits, data in card_data.items():
        cards_data.append(
            {
                "last_digits": last_digits,
                "total_spent": round(data["total_spent"], 2),
                "cashback": round(data["cashback"], 2),
            }
        )
    logger.info("получен словарь по тратам и кешбеку по каждой карте")
    return cards_data


def get_top_5_transactions(transactions: list[dict]) -> list[dict]:
    """Функция принимает список транзакций и выводит топ 5 операций по сумме платежа"""
    sorted_transactions = sorted(transactions, key=lambda x: abs(float(x["Сумма операции"])), reverse=True)
    top_5_sorted_transactions = []
    for transaction in sorted_transactions[:5]:
        date = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S").strftime("%d.%m.%Y")
        top_5_sorted_transactions.append(
            {
                "date": date,
                "amount": transaction["Сумма операции"],
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
        )
    logger.info("Выделено топ 5 больших транзакций")
    return top_5_sorted_transactions


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
