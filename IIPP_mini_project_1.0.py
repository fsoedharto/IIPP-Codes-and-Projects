# The program that implements and test the rock-paper-scissor-lizard-Spock game
#
# 
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors
#

# Mini Project 1
# Version 1.1 First implementation
# Version 1.2 Fixed the "no scissors bug" adding randrange
# to be 4
# Version 1.3 Added the case sensitive and checks valid
# input strings
# version 1.4 Added this documentation releases

# This version should have a bit less line of code
# Deleted the redundant number variable

import random

# Define the name_to_number function
# Converts the appropriate string into its numerical values above
# Makes a case insensitive naming of the string
def name_to_number(name):
    """
    Converts the input name taken into a number. This is
    not case sensitive.
    """
    if (name == 'rock' or name == 'Rock'):
        return 0
    elif (name == 'Spock' or name == 'spock'):
        return 1
    elif (name == 'paper' or name == 'Paper'):
        return 2
    elif (name == 'lizard' or name == 'Lizard'):
        return 3
    elif (name == 'scissors' or name == 'Scissors'):
        return 4
    else:
        return -1

# Convert the number chosen into its corresponding string name.
def number_to_name(number):
    """
    Converts the number representation of RPSLS into a string.
    """
    if (number == 0):
        name = 'rock'
        return name
    if (number == 1):
        name = 'Spock'
        return name
    if (number == 2):
        name = 'paper'
        return name
    if (number == 3):
        name = 'lizard'
        return name
    if (number == 4):
        name = 'scissors'
        return name
    else:
        print "ERROR: The choice of number is out of range!"

# Plays the game
# Takes input from the player and converts the player's 
# choice to a number. Randomly assigns the computer a number
# and decide who wins and prints the appropriate message.

def rpsls(player_choice):
    """
    This function plays the rock-paper-scissor-lizard-spock
    game.
    """
    
    # Convert the player's choice into numbers
    player_number = name_to_number(player_choice)

    # Prints error if input does not match any of the cases
    # and ends the game.
    if (player_number == -1):
        print "ERROR! Please choose either rock, paper, scissors, lizard, or Spock!\n"
        
    else:
        # Prints the player's choice and also converts the
        # upper/lowercase letters into its lower/uppercase 
        # letters
        print "Player chooses " + number_to_name(player_number)
    
        # Assigns a random choice for the computer's number
        comp_number = random.randrange(0,5)
    
        # Converts computer number into string
        comp_choice = number_to_name(comp_number)	

        # Converts computer's number into string
        print "Computer chooses " + comp_choice

        # Takes the difference between the computer's and player's number
        difference_modulo = (player_number - comp_number) % 5
    
        # Decide who wins based on the difference
        if (difference_modulo == 0):
            print "Player and computer tie!\n"
        elif (difference_modulo == 1 or difference_modulo == 2):
            print "Player wins!\n"
        else:
            print "Computer wins!\n"

# Test Output    

rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
rpsls("Rock")
rpsls("spock")
rpsls("Paper")
rpsls("Lizard")
rpsls("Scissors")
rpsls("Rcok")
rpsls("Fck")
