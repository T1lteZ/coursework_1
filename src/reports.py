import datetime
import json
import logging
from typing import Any, Callable, Optional

import pandas as pd

logger = logging.getLogger("report.log")
file_handler = logging.FileHandler("logs/reports.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def decorator_spending_by_category(func: Callable) -> Callable:
    """Логирует результат функции в файл по умолчанию decorator_spending_by_category.json"""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        with open("spending_by_category.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        return result

    return wrapper


def log_spending_by_category(filename: Any) -> Callable:
    """Логирует результат функции в указанный файл"""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs).to_dict("records")
            with open(filename, "w") as f:
                json.dump(result, f, indent=4)
            return result

        return wrapper

    return decorator


@decorator_spending_by_category
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None):
    """Функция возвращающая траты за последние 3 месяца по заданной категории"""
    logger.info("Начало работы")
    list_by_category = []
    final_list = []

    if date is None:
        logger.info("Обработка условия на отсутствие")
        date_start = datetime.datetime.now() - datetime.timedelta(days=90)
        for i in transactions:
            if i["Категория"] == category:
                list_by_category.append(i)
        for i in list_by_category:
            if i["Дата платежа"] == "nan" or type(i["Дата платежа"]) is float:
                continue
            elif (
                    date_start
                    <= datetime.datetime.strptime(str(i["Дата платежа"]), "%d.%m.%Y")
                    <= date_start + datetime.timedelta(days=90)
            ):
                final_list.append(i["Сумма платежа"])
        return final_list
    else:
        logger.info("Обработка условия на создание")
        day, month, year = date.split(".")
        date_obj = datetime.datetime(int(year), int(month), int(day))
        date_start = date_obj - datetime.timedelta(days=90)

        for i in transactions:
            if i["Категория"] == category:
                list_by_category.append(i)

        for i in list_by_category:
            if i["Дата платежа"] == "nan" or type(i["Дата платежа"]) is float:
                continue
            else:
                day_, month_, year_ = i["Дата платежа"].split(".")
                date_obj_ = datetime.datetime(int(year), int(month), int(day))
                if date_start <= date_obj_ <= date_start + datetime.timedelta(days=90):
                    final_list.append(i["Сумма платежа"])
        logger.info("Завершение работы функции")
        data_json = json.dumps(final_list, indent=4, ensure_ascii=False, )

        return data_json
