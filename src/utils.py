import datetime

import pandas as pd

from path_to_file import PATH_TO_FILE


def greetings():
    """Функция приветствия"""
    time_obj = datetime.datetime.now()
    if 6 <= time_obj.hour <= 12:
        return "Доброе утро"
    elif 13 <= time_obj.hour <= 18:
        return "Добрый день"
    elif 19 <= time_obj.hour <= 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def read_excel(PATH_TO_FILE: str) -> list[dict]:
    """Функция читает .xlsx файл и возвращает список словарей"""
    df = pd.read_excel(PATH_TO_FILE)
    result = df.apply(
        lambda row: {
            "Дата платежа": row["Дата платежа"],
            "Статус": row["Статус"],
            "Сумма платежа": row["Сумма платежа"],
            "Валюта платежа": row["Валюта платежа"],
            "Категория": row["Категория"],
            "Описание": row["Описание"],
            "Номер карты": row["Номер карты"],
        },
        axis=1,
    ).tolist()
    return result
