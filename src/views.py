import datetime
import json
import logging
import os
import sys
sys.path.append(os.getcwd())

import pandas as pd
import requests
from dotenv import load_dotenv

from path_to_file import PATH_TO_FILE

load_dotenv()

EXCHANGE_RATES_DATA_API = os.getenv("API_KEY_APILAYER")
df = pd.read_excel(PATH_TO_FILE)
df.columns = [
    "Transaction date",
    "Payment date",
    "Card number",
    "Status",
    "Transaction amount",
    "Transaction currency",
    "Payment amount",
    "Payment currency",
    "Cashback",
    "Category",
    "MCC",
    "Description",
    "Bonuses (including cashback)",
    "Rounding to the investment bank",
    "The amount of the operation with rounding",
]

views_logger = logging.getLogger("views")
file_handler = logging.FileHandler("logs/views.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
views_logger.addHandler(file_handler)
views_logger.setLevel(logging.INFO)


def greeting() -> str:
    """Функция вывода сообщения приветствия в зависимости от времени суток"""
    opts = {"greeting": ("доброе утро", "добрый день", "добрый вечер", "доброй ночи")}
    current_time = datetime.datetime.now()
    if current_time.hour >= 4 and current_time.hour <= 12:
        greet = opts["greeting"][0]
    elif current_time.hour >= 12 and current_time.hour <= 16:
        greet = opts["greeting"][1]
    elif current_time.hour >= 16 and current_time.hour <= 24:
        greet = opts["greeting"][2]
    else:
        greet = opts["greeting"][3]
    return greet


def exchange_rate(currency_list: list[str]) -> dict[str, [str | int]]:
    """Функция получения курса валют через API"""
    url = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": f"{EXCHANGE_RATES_DATA_API}"}
    currency_rate = []
    for currency in currency_list:
        payload = {"symbols": "RUB", "base": f"{currency}"}
        response = requests.get(url, headers=headers, params=payload)
        status_code = response.status_code
        if status_code == 200:
            res = response.json()
            currency_rate_dict = {"currency": f"{res['base']}", "rate": f"{res['rates']['RUB']}"}
            currency_rate.append(currency_rate_dict)
        else:
            print(f"Запрос не был успешным.")
            views_logger.info("Запрос не удался")
    views_logger.info("Данные по курсу валют успешно получены")
    return currency_rate


def card_info(date_string: str, DataFrame):
    """Функция отображения информации о карте в заданном формате"""
    try:
        date_string_dt_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
        start_date_for_sorting = date_string_dt_obj.replace(day=1)
        edited_df = DataFrame.drop(
            [
                "Payment date",
                "Transaction currency",
                "Payment amount",
                "Payment currency",
                "Cashback",
                "Category",
                "MCC",
                "Description",
                "Bonuses (including cashback)",
                "Rounding to the investment bank",
                "The amount of the operation with rounding",
            ],
            axis=1,
        )
        edited_df["Transaction date"] = edited_df["Transaction date"].apply(
            lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
        )
        filtered_df_by_date = edited_df.loc[
            (edited_df["Transaction date"] <= date_string_dt_obj)
            & (edited_df["Transaction date"] >= start_date_for_sorting)
            & (edited_df["Card number"].notnull())
            & (edited_df["Transaction amount"] <= 0)
            & (edited_df["Status"] != "FAILED")
        ]
        grouped_df = filtered_df_by_date.groupby(["Card number"], as_index=False).agg({"Transaction amount": "sum"})
        data_list = []
        for index, row in grouped_df.iterrows():
            data_dict = {
                "Card number": row["Card number"].replace("*", ""),
                "Transaction amount": round(row["Transaction amount"], 2),
                "cashback": round(row["Transaction amount"] / 100, 2),
            }
            data_list.append(data_dict)
        views_logger.info("Данные по картам успешно сформированны")
        return data_list
    except ValueError:
        print("Неверный формат даты")
        views_logger.error("Ошибка ввода данных: неверный формат даты")


def top_5_transactions(date_string: str, DataFrame):
    """Функция отображения топ 5 транзакций по сумме платежа"""
    date_string_dt_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
    start_date_for_sorting = date_string_dt_obj.replace(day=1)
    edited_df = DataFrame.drop(
        [
            "Payment date",
            "Card number",
            "Transaction currency",
            "Payment amount",
            "Payment currency",
            "Cashback",
            "MCC",
            "Bonuses (including cashback)",
            "Rounding to the investment bank",
            "The amount of the operation with rounding",
        ],
        axis=1,
    )
    edited_df["Transaction date"] = edited_df["Transaction date"].apply(
        lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
    )
    filtered_df_by_date = edited_df.loc[
        (edited_df["Transaction date"] <= date_string_dt_obj)
        & (edited_df["Transaction date"] >= start_date_for_sorting)
        & (edited_df["Transaction amount"].notnull())
        & (edited_df["Status"] != "FAILED")
    ]
    sorted_df_by_transaction_amount = filtered_df_by_date.sort_values(
        by=["Transaction amount"], ascending=False, key=lambda x: abs(x)
    )
    top_transactions = sorted_df_by_transaction_amount[0:5]
    data_list = []
    for index, row in top_transactions.iterrows():
        data_dict = {
            "date": row["Transaction date"].strftime("%d.%m.%Y"),
            "amount": round(row["Transaction amount"], 2),
            "category": row["Category"],
            "description": row["Description"],
        }
        data_list.append(data_dict)
    views_logger.info("Данные по топу транзакций успешно сформированны")
    return data_list
