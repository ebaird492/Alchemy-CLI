"""
===============================================================================
ENGR 13000 Fall 2022

Program Description
    The backend for a command line interface (CLI) Alchemy game

Assignment Information
    Assignment:     Project 4 - Backend
    Author:         Ethan Baird, baird28@purdue.edu
    Team ID:        LC1 - 03

ACADEMIC INTEGRITY STATEMENT
I have not used source code obtained from any other unauthorized
source, either modified or unmodified. Neither have I provided
access to my code to another. The project I am submitting
is my own original work.
===============================================================================
"""

class Alchemy:
    """A Command Line Interface for the game Alchemy"""

    def __init__(self, data):
        """Initialize Variables"""

        # the elements that the user starts off with
        self.start_items = ['air', 'earth', 'fire', 'water']
        self.avail_items = self.start_items[:] # items the user can use
        self.LINE_SPACING = " " * 2 # shift the text over with whitespace
        self.LINE_WIDTH = 90 # the maximum line width allowed for output
        # a dictionary that contains the definitions of all possible combos
        self.poss_combos = {} # the combos lead to discoveriess
        self.init_combos(data) # initialize all the data


    def init_combos(self, data):
        """Set the dictionary with the correct combos"""

        for item in data:
            key = item[0] # the result of a combination
            values = item[1] # what needs to be combined
            poss_items = [] # the items for each discovery
            if key not in self.avail_items:
                if "/" in values:
                    # create a list of the possible combinations to get the
                    # given key
                    poss_items = values.strip().split(" / ")

                    # make each combo into its own list
                    for i in range(len(poss_items)):
                        poss_items[i] = poss_items[i].strip('" ').split(", ")
                else:
                    poss_items = values.strip('" ').split(", ")

                # create a new dictionary entry
                self.poss_combos[key.lower()] = poss_items
    

    def welcome_user(self):
        """Intitial onboarding for user"""

        welcome = open("data/welcome.txt", "r")
        for line in welcome:
            print(self.LINE_SPACING + line.strip())
        welcome.close;


    def load_data(self):
        """Loads data from the save file into the available items"""

        load = open("data/save_data.txt", "r")
        for line in load:
            self.avail_items = line.strip().split(" ")
        print(self.LINE_SPACING + "DATA LOADED")

        load.close()

    
    def save_data(self, wipe_mem=0):
        """Save the current available items into memory"""

        save = open("data/save_data.txt", "w")
        if wipe_mem == 0: 
            save.write(" ".join(self.avail_items))
        else:
            save.write(" ".join(self.start_items))
        print(self.LINE_SPACING + "DATA SAVED")

        save.close()


    def error_handling(self, error_type):
        """Display a specific error due to user input"""

        error_str = self.LINE_SPACING + "###INVALID MOVE - "
        if error_type == "spacing":
            error_str += "incorrect spacing"
        elif error_type == "n_avail":
            error_str += "item(s) not in available items"
        elif error_type == "num_items":
            error_str += "incorrect number of items"
        elif error_type == "no_ans":
            error_str += "no items entered"
        print(error_str)


    def print_dict(self):
        """Print the dictionary values"""

        for keys, values in self.poss_combos.items():
            print("", keys, " : ", values)

    def print_avail(self):
        """Print the list of available items"""

        print(self.LINE_SPACING + f"Available Items {len(self.avail_items)} | "
        f"{len(self.poss_combos)} ::")
        print_str = "  "
        len_line = 0
        for i in range(len(self.avail_items)):
            len_line += len(self.avail_items[i])
            if len_line > self.LINE_WIDTH: # limit the line width
                print_str += "\n  " 
                len_line = 2 + len(self.avail_items[i])
            print_str += self.avail_items[i]
            if i < (len(self.avail_items) - 1):
                print_str += " / "
                len_line += 3
        print(print_str)


    def end_game(self):
        """
        Determines if the user has completed the game by finding all
        the discoveries
        """

        # all the items have been found
        if len(self.avail_items) == len(self.poss_combos) + len(self.start_items):
            print("\n\nYOU COMPLETED THE GAME!! All items have been discovered!")
            return True

        # the user found all of the possible discoveries
        return False


    def get_avail(self):
        """Return the available items"""

        return self.avail_items

    
    def combine_items(self, item1, item2):
        """Iterate through each entry in poss_combos to get the combinations"""

        valid = self.check_valid(item1, item2) # the items need to be available
        found_combo = False # has at least one combo been found?
        valid_combo = False # the items produce a combo
        new_items = [] # 

        if valid:
            for result, combo in self.poss_combos.items():
                result = result.replace(" ", "_")
                valid_combo = False
                # check if the result has already been found
                if result not in self.avail_items:
                    # if the first item is a list, each item needs to be iterated
                    if isinstance(combo[0], list):
                        for items in combo:
                            if valid_combo == False:
                                valid_combo = self.add_new(items, item1, item2, 
                                result)
                    else:
                        valid_combo = self.add_new(combo, item1, item2, result)
                    
                    if valid_combo:
                        # set the name of the combo to the given result
                        new_items.append(result)
                        found_combo = True
                    
            if found_combo:
                if len(new_items) > 1:
                    print(self.LINE_SPACING + "NEW ITEMS FOUND! : " + 
                        ", ".join(new_items))
                else:
                    print(self.LINE_SPACING + "NEW ITEM FOUND! : ",
                        new_items[0])
            else:
                print(self.LINE_SPACING + "NO NEW DISCOVERY")
        else:
            self.error_handling("n_avail")

    
    def check_valid(self, item1, item2):
        """Check if the inputted items are available"""

        if(item1 in self.avail_items and item2 in self.avail_items):
            return True
        return False


    def add_new(self, list_check, item1, item2, result):
        """
        Adds the new combo to available items if both given items make up
        the combo
        """

        # Checks if both given items are a possible combo

        item1 = item1.replace("_", " ") # spaces must be removed
        item2 = item2.replace("_", " ")
        condit = (list_check[0] == item1 and list_check[1] == item2) 
        condit = condit or (list_check[0] == item2 and list_check[1] == item1)
        if condit:
            # if a new item is discovered it gets added to the available items 
            self.avail_items.append(result)
        return condit