import json
import logging
from typing import Any, Callable

logger = logging.getLogger("services.log")
file_handler = logging.FileHandler("logs/services.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def decorator_search(func: Callable) -> Callable:
    """Логирует результат функции в файл по умолчанию decorator_search.json"""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        with open("search.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        return result

    return wrapper


@decorator_search
def simple_search(my_list: list, string_search: str):
    """Функция поиска по переданной строке"""
    result = []
    logger.info("Начало работы функции (simple_search)")
    if my_list == []:
        return []
    else:
        for i in my_list:
            if string_search == "":
                return result
            elif (
                i["Описание"] == "nan"
                or type(i["Описание"]) is float
                or i["Категория"] == "nan"
                or type(i["Категория"]) is float
            ):
                continue
            elif string_search in i["Описание"] or string_search in i["Категория"]:
                result.append(i)

        logger.info("Конец работы функции (simple_search)")
        data_json = json.dumps(result, indent=4, ensure_ascii=False)

        return data_json
