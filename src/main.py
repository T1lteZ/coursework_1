import json
import os
import sys
sys.path.append(os.getcwd())

import pandas as pd
from dotenv import load_dotenv

from path_to_file import PATH_TO_FILE
from src.views import card_info, exchange_rate, greeting, top_5_transactions

load_dotenv()

EXCHANGE_RATES_DATA_API = os.getenv("API_KEY_APILAYER")
df = pd.read_excel(PATH_TO_FILE)
with open("user_settings.json") as file:
    currency_rates = json.load(file)

date = input("Введите дату в формате YYYY-MM-DD HH:MM:SS: ")


def return_json_answer(df, date: str):
    """Главная функция выводящая результат запроса по дате"""
    info_by_transactions = {
        "greeting": greeting(),
        "cards": card_info(date, df),
        "top transactions": top_5_transactions(date, df),
        "currency rates": exchange_rate(currency_rates["user_currencies"]),
    }
    answer_in_json_format = json.dumps(info_by_transactions, indent=4, ensure_ascii=False)
    return answer_in_json_format
