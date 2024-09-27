import json
import os

import pandas as pd
from dotenv import load_dotenv

from path_to_file import PATH_TO_FILE, PATH_TO_FILE_USER
from reports import spending_by_category
from services import simple_search
from utils import read_excel
from views import main

with open(PATH_TO_FILE_USER, "r") as file:
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

    path = PATH_TO_FILE
    my_list = read_excel(path)
    user_string = input("Введите строку поиска:")
    if user_string == "":
        print(my_list)
    else:
        searching = simple_search(my_list, user_string)
        print(searching)

    df = pd.read_excel(PATH_TO_FILE)
    user_category = input("Введите категорию поиска:")
    if user_category == "":
        print([])
    else:
        spending_cat = spending_by_category(df, user_category, user_date)
        print(spending_cat)


if __name__ == "__main__":
    main_menu()
