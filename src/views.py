import json
import logging
import os
from typing import Any

import pandas as pd
from dotenv import load_dotenv

from src.utils import (
    currency_rates,
    filter_by_date,
    get_cards_data,
    get_price_stock,
    get_top_5_transactions,
    greetings,
    read_excel,
)

logger = logging.getLogger("views.log")
file_handler = logging.FileHandler("views.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


with open("C:/Users/stasf/PycharmProjects/coursework/user_settings.json", "r") as file:
    user_choice = json.load(file)
load_dotenv()
api_key_currency = os.getenv("API_KEY_VALUTE")
api_key_stocks = os.getenv("API_KEY_500")


def main(input_date: Any, user_settings: Any, api_key_currency: Any, api_key_stocks: Any) -> Any:
    """Основная функция для генерации JSON-ответа."""
    path = r"C:/Users/stasf/PycharmProjects/coursework/data/operations.xlsx"
    trans_pd = pd.read_excel(path)
    filtered_transactions = filter_by_date(trans_pd, input_date)
    cards_data = get_cards_data(filtered_transactions)
    exchange_rates = currency_rates(user_settings["user_currencies"], api_key_currency)
    stocks_cost = get_price_stock(user_settings["user_stocks"], api_key_stocks)
    top_transactions = get_top_5_transactions(filtered_transactions)
    greeting = greetings()
    user_data = {
        "greeting": greeting,
        "cards": cards_data,
        "top_transactions": top_transactions,
        "exchange_rates": exchange_rates,
        "stocks": stocks_cost,
    }
    return json.dumps(user_data, ensure_ascii=False, indent=4)
