from env_stash import success
import letter.entrypoint_letter
from web_interaction.web_entrypoint import main as parse_main


if __name__ == "__main__":
    print(success)
    print("Mind the gap!\n")
    work_type = bool(input("1 for parse, 0 for letter constructor only\n"))

    if not work_type:
        while True:
            try:
                letter.entrypoint_letter.main()
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
    else:
        parse_main(int(input("1 for tg, 2 for hh, 3 for linkedIn(not yet)\n")))
