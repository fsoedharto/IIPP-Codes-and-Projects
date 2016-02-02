# Mini Project 3 Stopwatch Game
# 
# Every whole number, click Stop on the right moment and
# increment score and the total number of clicks. Display 
# the time and the score on the canvas where the time is
# in the form 0:00.0 (Mins:Secs.TenthSecs) and the score
# is (correct clicks / total clicks)

import simplegui

##########################################################
# Define Global Variables

# Set the dimensions of the frame
width = 250
height = 250

# Variable that keeps track of every 0.1 seconds
time = 0

# Stores the time string that will be displayed on canvas
message = '0:00.0'

# Count the correctly timed click of the stop button
count = 0

# Counts the total number of stops throughout the game
total_click = 0

# Shows the 'correct' clicks out of the total number of
# clicks on the canvas
score = 'Score: 0 / 0'

# This variable prevents the number of stop button clicks
# to increase when the game is stopped and before the game
# starts
start_flag = 0

# Prints additional messages
message1 = 'Click Stop at every 1.0 seconds!'

##########################################################
# Define Functions

# Prints the timer and the 'score' and timer on the screen
# as well other message below all in Red
def draw(canvas):
    """
    This function is the draw handler.
    """
    
    # Prints the "Click at every 1.0 seconds"
    canvas.draw_text(message1, (10,20), 18, "Green")
    
    # Prints the constantly updated timer
    canvas.draw_text(message, (90, 130), 30, "White")
    
    # Prints the score (correct clicks / 
    # total clicks)
    canvas.draw_text(score, (15, 240), 30, "Yellow")

# Define a click handler that counts the number of on time
# stops and total stop clicks and prints a the score to be
# displayed on the canvas
def click():
    """
    This function is a mouse click handler.
    """
    
    # Define global variables
    global total_click
    global count
    global score
    
    # Check whether the time is at a multiple of a 
    # second then increment the on time click count and 
    # total click count, else just increment total click 
    # count
    if (time % 10) == 0:
        count += 1
    
    # Increment the total_click count
    total_click += 1

    # Updates the score string
    score = 'Score: ' + str(count) + ' / ' + \
    str(total_click)

# Time handler function
def time_handler():
    """
    This function increments the time at the start of the
    game and keeps incrementing the time every 0.1 seconds
    calls the format function which process the global
    variable time into a string.    
    """
    global time
    time += 1
    format()

# Processes the global variable time into a string which
# will be displayed as a message on the canvas
def format():
    """
    This function formats the global variables of time
    into a string in the format of MM:SS.T
    """
    
    # Define global variable
    global message
    
    # Take 0.1 seconds
    tenths_second = str(int(time % 10))
    
    # Temporary variable to store the number 
    # of seconds
    second_temp = int(time / 10) % 60
    
    # Divides the seconds into tens and ones digit
    ten_second = str(int(second_temp / 10) % 6)
    one_second = str(second_temp % 10)
    
    # Concatenates the tens, ones, and tenths 
    # of a second into a string
    seconds = ten_second + one_second + "." + \
    tenths_second
    
    # Converts time into minutes (e.g. time = 
    # 600 = 60 sec = 1 min)
    minutes = str(int(time / 600))
    
    # Concatenate the minutes and seconds strings to be
    # displayed on the canvas
    message = minutes + ":" + seconds

# Starts timer on the click of the start game button
def start_game():
    """
    This function stars the timer on the click of a
    button.
    """
    # Declare global variable
    global start_flag
    
    # Start the timer
    timer.start()
    
    # Allows the number of stop button
    # clicks to increment
    start_flag = 1

# A function to stop the game
def stop_game():
    """
    Stops the timer on the click of the button and calls
    the click handler to increment click count and
    'on time' count on the press of the stop button
    This function will not increment the count if the game
    has not started or if the game is stopped.
    """
    
    # Declares global variable
    global start_flag

    # Check if start_flag is true. If true, then 
    # increment the score count. This prevents the 
    # number of stop button clicks to increase when 
    # the game is stopped and also before the game 
    # is started
    if start_flag:
        click()
    timer.stop()
    start_flag = 0

# Resets the timer to 0:00.0 and score to 0/0
def reset_game():
    """
    This is a button helper function that resets the score,
    timer to zero.
    """
    
    # Declare global variables
    global time
    global count
    global total_click
    global message
    global score
    global start_flag
    
    # Resets global variable time, count, total click, 
    # and the start_flag
    time = 0
    count = 0
    total_click = 0
    start_flag = 0
    
    # Resets the timer display and score and 
    # stops time
    message = '0:00.0'
    score = 'Score: 0 / 0'
    timer.stop()
    
##########################################################
# Create frame


frame = simplegui.create_frame("Stopwatch Game",\
                               width, height)

##########################################################
# Add Buttons


frame.add_button("Start", start_game, 100)
frame.add_button("Stop", stop_game, 100)
frame.add_button("Reset", reset_game, 100)

##########################################################
# Set Draw Handler


frame.set_draw_handler(draw)

##########################################################
# Adds timer


timer = simplegui.create_timer(100, time_handler)

##########################################################
# Start the frame

frame.start()
