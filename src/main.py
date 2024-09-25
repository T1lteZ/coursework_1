import json
import os
import sys
sys.path.append(os.getcwd())
import pandas as pd
from dotenv import load_dotenv

from reports import spending_by_category
from services import simple_search
from utils import read_excel
from views import main

with open("C:/Users/stasf/PycharmProjects/coursework/user_settings.json", "r") as file:
    user_choice = json.load(file)
load_dotenv()
api_key_currency = os.getenv("API_KEY_VALUTE")
api_key_stocks = os.getenv("API_KEY_500")


def main_menu():
    user_date = input("Введите дату:")
    if user_date == "":
        print([])
    else:
        main_page = main(user_date, user_choice, api_key_currency, api_key_stocks)
        print(main_page)

    path = r"C:/Users/stasf/PycharmProjects/coursework/data/operations.xlsx"
    my_list = read_excel(path)
    user_string = input("Введите строку поиска:")
    if user_string == "":
        print(my_list)
    else:
        searching = simple_search(my_list, user_string)
        print(searching)

    df = pd.read_excel(r"C:/Users/stasf/PycharmProjects/coursework/data/operations.xlsx")
    user_category = input("Введите категорию поиска:")
    if user_category == "":
        print([])
    else:
        spending_cat = spending_by_category(df, user_category, user_date)
        print(spending_cat)


if __name__ == "__main__":
    main_menu()
