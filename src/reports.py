import datetime
import json
import logging
import os

import pandas as pd

PATH_TO_FILE = os.path.join(os.path.dirname(__file__), "../data", "operations.xlsx")
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

utils_logger = logging.getLogger("reports")
file_handler = logging.FileHandler("logs/reports.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)
utils_logger.setLevel(logging.INFO)


def average_cost_amount(data_frame, date=datetime.date.today()):
    """Функция возвращающая среднее значение трат за день за последние 3 месяца от введённой даты"""
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    start_date_for_counting = date - datetime.timedelta(days=90)
    data_frame["Transaction date"] = data_frame["Transaction date"].apply(
        lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
    )
    filtered_df = data_frame.loc[
        (data_frame["Transaction date"] <= date)
        & (data_frame["Transaction date"] >= start_date_for_counting)
        & (data_frame["Transaction amount"] < 0)
    ]
    grouped_df_by_date = filtered_df.groupby(["Transaction date"], as_index=False).agg({"Transaction amount": "mean"})
    data_dict = grouped_df_by_date.to_dict(orient="records")
    avg_amount_spent = []
    for element in data_dict:
        avg_spent = {
            "Transaction date": element["Transaction date"].strftime("%d.%m.%Y"),
            "Average amount spent": round(element["Transaction amount"], 2),
        }
        avg_amount_spent.append(avg_spent)
    utils_logger.info("Средние траты за день за последние 3 месяца успешно сформированы")
    return json.dumps(avg_amount_spent, indent=4, ensure_ascii=False)
