import csv
from functools import wraps
import logging
import json
from datetime import datetime, timedelta
from typing import Any, Callable, Optional

import pandas as pd

logger = logging.getLogger("report.log")
file_handler = logging.FileHandler("logs/reports.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def log_spending_by_category(filename: Any) -> Callable:
    """Логирует результат функции в указанный файл"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4)
            return result

        return wrapper

    return decorator


@log_spending_by_category("data/report_output.json")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращающая траты за последние 3 месяца по заданной категории"""
    try:
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        if date is None:
            date = datetime.now()
        else:
            date = datetime.strptime(date, "%d.%m.%Y")
        start_date = date - timedelta(days=date.day - 1) - timedelta(days=3 * 30)
        filtered_transactions = transactions[
            (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= date)
            & (transactions["Категория"] == category)
        ]
        grouped_transactions = filtered_transactions.groupby(pd.Grouper(key="Дата операции", freq="ME")).sum()
        logger.info(f"Траты за последние три месяца от {date} по категории {category}")
        results = grouped_transactions.to_json(orient="records")
        json_obj = json.loads(results)
        return json_obj
    except Exception as e:
        print(f"Возникла ошибка {e}")
        logger.error(f"Возникла ошибка {e}")
        return ""
