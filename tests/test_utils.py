from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest


from src.utils import (filter_by_date, get_cards_data, get_top_5_transactions, greetings, read_excel)


ROOT_PATH = Path(__file__).resolve().parent.parent


def test_get_data_from_xlsx():
    test_data = [
        {
            "Дата операции": "01.06.2023 12:00:00",
            "Сумма операции": "-100.50",
            "Категория": "Покупки",
            "Описание": "Магазин",
        },
        {
            "Дата операции": "15.06.2023 18:30:00",
            "Сумма операции": "-250.00",
            "Категория": "Ресторан",
            "Описание": "Ужин",
        },
    ]
    df = pd.DataFrame(test_data)
    with patch("pandas.read_excel", return_value=df):
        result = read_excel(r"../data/operations.xls")
        assert result == test_data


@pytest.fixture
def test_transactions():
    return [
        {
            "Дата операции": "01.06.2023 12:00:00",
            "Сумма операции": "-100.50",
            "Категория": "Покупки",
            "Описание": "Магазин",
        },
        {
            "Дата операции": "15.06.2023 18:30:00",
            "Сумма операции": "-250.00",
            "Категория": "Ресторан",
            "Описание": "Ужин",
        },
        {
            "Дата операции": "20.06.2023 10:00:00",
            "Сумма операции": "-75.00",
            "Категория": "Транспорт",
            "Описание": "Такси",
        },
        {
            "Дата операции": "05.05.2023 08:15:00",
            "Сумма операции": "-500.00",
            "Категория": "Медицина",
            "Описание": "Аптека",
        },
        {
            "Дата операции": "25.05.2023 14:45:00",
            "Сумма операции": "-120.00",
            "Категория": "Покупки",
            "Описание": "Одежда",
        },
    ]


@pytest.mark.parametrize(
    "input_date_str, expected_result",
    [
        (
            "20.06.2023",
            [
                {
                    "Дата операции": "01.06.2023 12:00:00",
                    "Сумма операции": "-100.50",
                    "Категория": "Покупки",
                    "Описание": "Магазин",
                },
                {
                    "Дата операции": "15.06.2023 18:30:00",
                    "Сумма операции": "-250.00",
                    "Категория": "Ресторан",
                    "Описание": "Ужин",
                },
                {
                    "Дата операции": "20.06.2023 10:00:00",
                    "Сумма операции": "-75.00",
                    "Категория": "Транспорт",
                    "Описание": "Такси",
                },
            ],
        ),
        (
            "15.05.2023",
            [
                {
                    "Дата операции": "05.05.2023 08:15:00",
                    "Сумма операции": "-500.00",
                    "Категория": "Медицина",
                    "Описание": "Аптека",
                },
            ],
        ),
    ],
)
def test_filter_transactions_by_date(test_transactions, input_date_str, expected_result):
    result = filter_by_date(test_transactions, input_date_str)
    assert result == expected_result


@patch("src.utils.datetime")
@pytest.mark.parametrize(
    "current_hour, expected_greeting",
    [
        (7, "Доброе утро"),
        (13, "Добрый день"),
        (19, "Добрый вечер"),
        (2, "Доброй ночи"),
    ],
)
def test_greeting(mock_datetime, current_hour, expected_greeting):
    mock_now = datetime(2023, 6, 20, current_hour, 0, 0)
    mock_datetime.now.return_value = mock_now
    result = greetings()
    assert result == expected_greeting


def test_get_cards_data_empty():
    transactions = []
    expected_result = []
    assert get_cards_data(transactions) == expected_result


def test_get_top_5_transactions_empty():
    transactions = []
    expected_result = []
    assert get_top_5_transactions(transactions) == expected_result


def test_get_top_5_transactions_single_transaction():
    transactions = [
        {
            "Дата операции": "20.06.2023 12:00:00",
            "Сумма операции": "-100.0",
            "Категория": "Еда",
            "Описание": "Покупка еды",
        }
    ]
    expected_result = [{"date": "20.06.2023", "amount": "-100.0", "category": "Еда", "description": "Покупка еды"}]
    assert get_top_5_transactions(transactions) == expected_result


def test_get_top_5_transactions_multiple_transactions():
    transactions = [
        {
            "Дата операции": "20.06.2023 12:00:00",
            "Сумма операции": "-100.0",
            "Категория": "Еда",
            "Описание": "Покупка еды",
        },
        {
            "Дата операции": "21.06.2023 12:00:00",
            "Сумма операции": "-200.0",
            "Категория": "Транспорт",
            "Описание": "Оплата проезда",
        },
        {
            "Дата операции": "22.06.2023 12:00:00",
            "Сумма операции": "-50.0",
            "Категория": "Развлечения",
            "Описание": "Кино",
        },
        {
            "Дата операции": "23.06.2023 12:00:00",
            "Сумма операции": "-300.0",
            "Категория": "Магазины",
            "Описание": "Покупка одежды",
        },
        {
            "Дата операции": "24.06.2023 12:00:00",
            "Сумма операции": "-20.0",
            "Категория": "Кофе",
            "Описание": "Кофе на вынос",
        },
        {
            "Дата операции": "25.06.2023 12:00:00",
            "Сумма операции": "-400.0",
            "Категория": "Магазины",
            "Описание": "Покупка техники",
        },
    ]
    expected_result = [
        {"date": "25.06.2023", "amount": "-400.0", "category": "Магазины", "description": "Покупка техники"},
        {"date": "23.06.2023", "amount": "-300.0", "category": "Магазины", "description": "Покупка одежды"},
        {"date": "21.06.2023", "amount": "-200.0", "category": "Транспорт", "description": "Оплата проезда"},
        {"date": "20.06.2023", "amount": "-100.0", "category": "Еда", "description": "Покупка еды"},
        {"date": "22.06.2023", "amount": "-50.0", "category": "Развлечения", "description": "Кино"},
    ]
    assert get_top_5_transactions(transactions) == expected_result


def test_get_top_5_transactions_less_than_5():
    transactions = [
        {
            "Дата операции": "20.06.2023 12:00:00",
            "Сумма операции": "-100.0",
            "Категория": "Еда",
            "Описание": "Покупка еды",
        },
        {
            "Дата операции": "21.06.2023 12:00:00",
            "Сумма операции": "-200.0",
            "Категория": "Транспорт",
            "Описание": "Оплата проезда",
        },
    ]
    expected_result = [
        {"date": "21.06.2023", "amount": "-200.0", "category": "Транспорт", "description": "Оплата проезда"},
        {"date": "20.06.2023", "amount": "-100.0", "category": "Еда", "description": "Покупка еды"},
    ]
    assert get_top_5_transactions(transactions) == expected_result
