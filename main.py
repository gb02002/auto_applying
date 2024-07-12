from logic import start_logic
from texts import my_dict
from pyperclip import copy


def main():
    lang = int(input("Type 1 for eng and 2 for rus: "))
    type_str = str(input(f"Input type of companies such as {list(my_dict.keys())}: "))
    if type_str:
        type_of_company = my_dict[type_str]
        res = start_logic(type_of_company, lang)
        copy(res)
        return


if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyError:
            print("Error: Wrong key used.")
        except TypeError:
            print("Error: Unexpected type of value.")
        except ValueError:
            print("Error: Wrong type of input.")
        except KeyboardInterrupt:
            print("\nAll good, goodbye!")
            break  # Use break to exit the loop gracefully
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
