from pyperclip import copy

from letter.logic import start_logic
from letter.texts import my_dict


def main():
    lang = int(input("Type 1 for eng and 2 for rus: "))
    type_str = str(input(f"Input type of companies such as {list(my_dict.keys())}: "))
    if type_str:
        type_of_company = my_dict[type_str]
        res = start_logic(type_of_company, lang)
        # copy(res)
        return res
