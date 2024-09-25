import json
import pytest
from src.utils import read_excel
from src.services import simple_search

path = r"C:/Users/stasf/PycharmProjects/coursework/data/operations.xlsx"
my_list = read_excel(path)
empty_list = []


@pytest.mark.parametrize("transactions, search, expected_output", [
    (
        [
            {"Категория": "Продукты", "Описание": "Покупка в магазине", "Сумма операции": -1000},
            {"Категория": "Развлечения", "Описание": "Кинотеатр", "Сумма операции": -500},
            {"Категория": "Транспорт", "Описание": "Такси", "Сумма операции": -300},
        ],
        "магазин",
        json.dumps([
            {"Категория": "Продукты", "Описание": "Покупка в магазине", "Сумма операции": -1000}
        ], ensure_ascii=False, indent=4)
    ),
    (
        [
            {"Категория": "Продукты", "Описание": "Покупка в магазине", "Сумма операции": -1000},
            {"Категория": "Развлечения", "Описание": "Кинотеатр", "Сумма операции": -500},
            {"Категория": "Транспорт", "Описание": "Такси", "Сумма операции": -300},
        ],
        "Продукты",
        json.dumps([
            {"Категория": "Продукты", "Описание": "Покупка в магазине", "Сумма операции": -1000}
        ], ensure_ascii=False, indent=4)
    ),
])
def test_search_transactions_by_user_choice(transactions, search, expected_output):
    result = simple_search(transactions, search)
    assert result == expected_output


def test_services_empty_attribute():
    assert simple_search(my_list, "") == []
