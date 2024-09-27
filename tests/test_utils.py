from datetime import datetime
from unittest.mock import patch
import pandas as pd
import pytest


from src.utils import (get_top_5_transactions, greetings, read_excel)


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


def test_get_top_5_transactions_empty():
    transactions = []
    expected_result = []
    assert get_top_5_transactions(transactions) == expected_result
