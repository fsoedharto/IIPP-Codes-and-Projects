# Mini-Project 2 "Guess the Number"
# Version Releases
# 2.1 First release 
# 2.2 Add some comments
# 2.3 Clears text after each game and add automatic play
# and adds two more higher range of an order of magnitude.
# 2.4 Resets when the computer play button is pressed and
# continues the game

import simplegui
import random
import math

#########################################################
# Global Variables


# Initialize the number of guesses
num_guess = 0

# Initializes secret number
secret_number = 47

# Initializes the range
num_range = 100

# Initializes the global variable status
hlc_value = 0

# Initializes the guess (Machine Only)
low = 0
high = 0

# Initialize reset_flag (will be used for the machines)
reset_flag = 0

#########################################################
# Define Functions


# Helper function that helps with computing the number of
# available guesses num_guess and secret_number
def new_game():
    """
    This function computes the available number of guess
    based on the range of inputs.
    """
    
    # Declare global variables
    global num_guess
    global secret_number
    
    # Computes the available number of guess given range
    # of numbers and define the maximum number of guesses
    num_guess = int(math.ceil(math.log(num_range + 1, 2)))
    
    # Randomly assigns the number within the appropriate
    # range into the secret_number from 0 to num_range - 1
    secret_number = random.randrange(0, num_range)
    
    # Prints new game, the range of numbers, and the
    # remaining number of guesses
    print "New game. Range is from 0 to", num_range
    print "Number of remaining guesses is", num_guess, "\n"

# This function re-starts the game with ranges [0, 100)
# on the click of the button for the range [0, 100)
def range100():
    """
    This function is for playing the game between the range
    of [0, 100)
    """
    
    # Declare global variable
    global num_range
    global low
    global high
    num_range = 100
    low = 0
    high = num_range
    
    # Calls helper function new game
    new_game()

# This function re-starts the game with ranges [0, 1000)
# on the click of the button for the range [0, 1000)
def range1000():
    """
    This function is for playing the game between the range
    of [0, 1000)
    """
    
    # Declare global variable for the range of numbers
    global num_range
    global low
    global high
    num_range = 1000
    low = 0
    high = num_range
    
    # Calls the helper function new game
    new_game()

# This function re-starts the game with ranges [0, 10000)
# on the click of the button for the range [0, 10000)
def range10000():
    """
    This function is for playing the game between the range
    of [0, 10000)
    """
    
    # Declare global variable for the range of numbers
    global num_range
    global low
    global high
    num_range = 10000
    low = 0
    high = num_range
    
    # Calls the helper function new game
    new_game()

def range100000():
    """
    This function is for playing the game between the range
    of [0, 100000)
    """
    
    # Declare global variable for the range of numbers
    global num_range
    global low
    global high
    num_range = 100000
    low = 0
    high = num_range
    
    # Calls the helper function new game
    new_game()
    
# Handler for the input function
# Checks whether the string is a number
# Prints higher, lower, or correct depending on guesses
# Prints the number of chances and restart game if 
# the correct number is guessed or ran out of chances
def input_guess(number):
    """
    This function checks the number with a hidden
    secret number and outputs whether the number chosen
    is lower or higher than the secret number. This
    number also checks whether it is a digit to prevent
    errors.
    """
    global num_guess
    global hlc_value
    global reset_flag
    
    # Check whether the string is a number and proceed
    # with the game
    if str.isdigit(number):
        
        # Decrement the number of remaining attempts
        num_guess -= 1
        
        # Prints the guess and the number of remaining 
        # guesses
        print "Guess is", number
        print "Number of remaining guesses is", num_guess
    
        # Print correct if guess is right
        # player that a new game must begin
        if int(number) == secret_number:
            print "Correct!\n"
            hlc_value = 0
            new_game()
    
        # Check if number of guesses ran out
        # Set the reset flag to 1 to inform the computer
        # Prints message and secret number
        # and restarts the game
        elif num_guess == 0:
            print "You ran out of guesses! The " \
                  "number is", secret_number, "\n"
            reset_flag = 1
            new_game()
        
        # Print higher if guess is lower than the 
        # secret number.
        elif int(number) < secret_number:
            print('Higher!\n')
            hlc_value = 1
            
        # Print lower if guess is higher than the 
        # secret number.
        else:
            print('Lower!\n')
            hlc_value = -1
    
    # If inputs entered are not numbers (positive integers)
    # then print error message and remaining guesses and
    # continue with the game
    else:
        print "ERROR! Please enter a positive integer\n" \
              "Number of remaining guesses " \
              "is", num_guess, "\n"

    # Resets the input text to blank
    guess.set_text('')

# Button handler that automatically plays the game
def binary_search():
    """
    This function is a button handler that automatically
    plays the game using binary search tree.
    """
    
    # Declare global variables
    global low
    global high
    global reset_flag

    # Puts initial guess by taking the midpoint
    initial_guess = int(math.ceil((low + high) / 2))

    # Resets the game if the number of remaining guesses
    # goes to zero resets the reset flag
    if reset_flag == 1:
        
        reset_flag = 0
        low = 0
        high = num_range
        binary_search()

    else:

        # Input the guesses
        input_guess(initial_guess)
    
        # Checks for high, low, and correct cases
        # For both low and high cases, the computer keeps
        # playing the game
        # If outputs higher then set the lower bound 
        # to the guessed number (hlc_value == 1)
        # If outputs lower then set the higher bound 
        # to the guessed number (hlc_value == -1)
        # If correct, then the game should end 
        # (hlc_value == 0)
        if hlc_value == 1:
            low = initial_guess
            binary_search()
        elif hlc_value == -1:
            high = initial_guess
            binary_search()
        else:
            high = num_range
            low = 0
            reset_flag = 0

# Executes the computer game
def computer_play():
    """
    Executes the computer game.
    """
    new_game()
    binary_search()
    
#########################################################
# Create the frame


frame = simplegui.create_frame("Guess the Number", 200, 200)

#########################################################
# Add Controls


# Add buttons for the [0,100) to [0,1000) ranges, and also
# other ranges 
frame.add_button('Range is [0,100)', range100, 200)
frame.add_button('Range is [0, 1000)', range1000, 200)
frame.add_button('Range is [0, 10000)', range10000, 200)
frame.add_button('Range is [0, 100000)', range100000, 200)

# Add another button for automatic guessing
frame.add_button('Computer Play', computer_play, 200)

# Add input
# Only accepts positive integers (1.0 is not valid)
guess = frame.add_input('Enter your guess:', input_guess, 200)

#########################################################
# Start the frame


frame.start()

#########################################################
# Start the game in the range 0 to 100


range100()
