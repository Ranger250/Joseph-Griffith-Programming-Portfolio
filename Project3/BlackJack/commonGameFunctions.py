def ask_yes_no(question):
    while True:
        answer = input(question)
        if "y" in answer.lower() and "n" in answer.lower():
            print("Not a valid option")
            continue
        elif "y" in answer.lower():
            answer = "yes"
            return answer
        elif "n" in answer.lower():
            answer = "no"
            return answer
        else:
            print("Not a valid option")


def flip_coin():
    import random
    result = random.choice["Heads", "Tails"]
    return result


def roll_die(die_sides):
    import random
    result = random.randint(1, int(die_sides))
    return result


def get_num_in_range(question, low, high):
    """aks the user for a number between a range and returns that number"""
    while True:
        answer = input(question)
        try:
            answer = int(answer)
            if answer >= low:
                if answer <= high:
                    return int(answer)
                else:
                    print("too high")
            else:
                print("too low")

        except:
            print("not a valid option")


def get_name(max_characters):
    """asks and returns users name"""
    name = input("Enter your name ")
    while True:
        if len(name) <= max_characters:
            return name
        else:
            print("too long")


def random_card():
    """gets a random card from a standard deck"""
    import random
    card_types = ["diamonds", "hearts", "spades", "clubs"]
    card_numbers = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
    card_type = random.choice(card_types)
    card_number = random.choice(card_numbers)
    card = card_number + " of " + card_type
    print(card)


def pick_from_menu(options):
    """takes in a list of options and asks the player which they would like to do."""
    while True:
        for i in range(len(options)):
            print(str(i + 1) + " " + options[i])
        answer = input("What would you like to do? ")
        try:
                answer = int(answer)
                if answer <= len(options) and answer > 0:
                    return answer
                else:
                    print("Invalid input, press enter to try again.\n")


        except:
            print("Invalid input , press enter to try again.\n")

if __name__ == "__main__":
    print("this is not a program try importing and using the classes")
    input("\n\nPress the enter key to exit.")
