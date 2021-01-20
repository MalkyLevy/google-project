from init import *
from complete import *


def main():
    print("Loading the files and prepaering the system...")
    data = init_data()

    while 1:
        user_input = input("Enter your text:\n")

        if user_input == "":
            break

        while '#' not in user_input:
            res = get_best_k_completions(user_input, data)
            print(f"Here are {len(res)} suggestions:")

            for i, l in enumerate(res, 1):
                print(f"{i}.", end=" ")
                l.auto_comp_print()

            user_input += input(f"{user_input}")

    print("\nExit")


main()
