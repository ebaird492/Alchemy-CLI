"""
===============================================================================
ENGR 13000 Fall 2022

Program Description
    The user interface for a command line interface (CLI) version of the game
    Alchemy

Assignment Information
    Assignment:     Project 4 - UI
    Author:         Ethan Baird, baird28@purdue.edu
    Team ID:        LC1 - 03

ACADEMIC INTEGRITY STATEMENT
I have not used source code obtained from any other unauthorized
source, either modified or unmodified. Neither have I provided
access to my code to another. The project I am submitting
is my own original work.
===============================================================================
"""

import os
from time import sleep
from alchemy import Alchemy

def main():
    # alchemy_data stores the possible combinations for the game
    # Initial data obtained from Little Alchemy created by Recloak:
    # https://www.ign.com/wikis/little-alchemy/Little_Alchemy_Cheats_-_
    # List_of_All_Combinations
    combo_txt = open("data/alchemy_data.txt", "r")

    # data will hold the various combinations
    data = []
    # clean the data
    for line in combo_txt:
        data.append(line.strip().split("\t"))
    combo_txt.close()

    game = Alchemy(data)
    continue_game = True

    while game.end_game() == False and continue_game == True:
        os.system("cls")
        game.welcome_user()
        game.print_avail()

        input_str = "\n  What are your two items (separated by a space)? "
        combo_input = input(input_str).strip()
        if combo_input == "q": # exit command
            continue_game = False
        elif combo_input == "load" or combo_input == "save":
            if combo_input == "load":
                game.load_data() # load from storage
            else:
                game.save_data() # save current file to storage
            sleep(.8)
        elif combo_input == "clear_mem":
            game.save_data(1) # clear memory
        else:
            if " " in combo_input:
                # each word should be separated by a space
                combo_input = combo_input.split(" ")
                if len(combo_input) > 2:
                    # only two items are allowed
                    game.error_handling("num_items")
                else:
                    # try to combine the items if the input is valid
                    game.combine_items(combo_input[0].strip(), combo_input[1].strip())
            elif combo_input == "":
                # nothing was entered
                game.error_handling("no_ans")
            else:
                # no space was used in the input
                game.error_handling("spacing")

            sleep(1.5)


if __name__ == "__main__":
    main()

