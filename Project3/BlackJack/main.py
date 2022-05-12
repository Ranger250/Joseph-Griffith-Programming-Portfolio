# Joseph Griffith

# BlackJack

# imports
from blackjackClasses import *
from commonGameFunctions import *

import random


def main():
    print("\t\tWelcome to Blackjack!\n")
    names = []
    number = get_num_in_range("How many players?  (1 - 7): ", low=1, high=8)
    for i in range(number):
        name = input("enter the player's name: ")
        names.append(name)
    game = Bj_Game(names)
    again = None
    while again != "no":
        game.play()
        again = ask_yes_no("\nDo you want to play again?: ")



main()
