# Mini Project 4
# Implementation of classic arcade game Pong (Simplified)
#

import simplegui
import random

############################################################
# Global Variables


# Assign The Canvas Dimensions
WIDTH = 600
HEIGHT = 400

# Assign Pad and Ball Dimensions
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

# Assign the logic value for the directions
LEFT = False
RIGHT = True

# Initizie paddle velocities
paddle1_vel = 0
paddle2_vel = 0

# Initialize player's scores
score1 = 0
score2 = 0

# Initialize ball position
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]

# Initialize paddle position
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2

# Game in Progress Flag
game_in_progress = 0

############################################################
# Define Functions and Event Handlers


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    """
    This function initializes the ball position and ball
    velocity.
    """
    
    # Initialize Global Variable
    # Ball Position and Ball Velocity
    global ball_pos, ball_vel
    
    # Assign random initial velocities to the ball
    ball_vel[0] = random.randrange(120, 240) / 60
    ball_vel[1] = -random.randrange(60, 180) / 90
    
    # Position the ball in the middle
    ball_pos[0] = WIDTH / 2
    ball_pos[1] = HEIGHT / 2
    
    # Throw starting ball to the left side
    if (direction == LEFT):
        ball_vel[0] = -ball_vel[0]
        
# Reset the game scores, ball positions, and paddle positions
def new_game():
    """
    This function initializes the score, paddle position,
    ball velocity.
    """
    
    # Declare global variables
    global paddle1_pos, paddle2_pos, paddle1_vel, \
    paddle2_vel
    
    # Declare global variables as integers
    global score1, score2
    
    # Resets the scores, paddle positions and speed
    paddle1_vel = 0
    paddle2_vel = 0
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    score1 = 0
    score2 = 0
    
    # Resets the ball position and velocity
    ball_pos[0] = WIDTH / 2
    ball_pos[1] = HEIGHT / 2
    ball_vel[0] = 0
    ball_vel[1] = 0

# Draw the scores, paddle position, ball position on the
# canvas
def draw(canvas):
    """
    This function is the draw handler that handles the scores,
    paddle position, ball position.
    """
    # Declare global variables
    global score1, score2, paddle1_pos, paddle2_pos, \
    ball_pos, ball_vel
    
    
    # Draw the mid-line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT],\
                     1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT],\
                     1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],\
                     [WIDTH - PAD_WIDTH, HEIGHT], 1,\
                     "White")
        
    # update ball position
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, \
                       'White', 'White')
    
    # update first paddle's vertical position, 
    # keep paddle on the screen
    paddle1_pos = paddle1_pos + paddle1_vel
    if (paddle1_pos + HALF_PAD_HEIGHT >= HEIGHT):
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    elif (paddle1_pos - HALF_PAD_HEIGHT <= 0):
        paddle1_pos = HALF_PAD_HEIGHT
    
    # update second paddle's vertical position,
    # keep paddle on the screen
    paddle2_pos = paddle2_pos + paddle2_vel
    if (paddle2_pos + HALF_PAD_HEIGHT >= HEIGHT):
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
    elif (paddle2_pos - HALF_PAD_HEIGHT <= 0):
        paddle2_pos = HALF_PAD_HEIGHT
    
    # draw first paddle
    canvas.draw_line([HALF_PAD_WIDTH, \
                      paddle1_pos - HALF_PAD_HEIGHT], \
                     [HALF_PAD_WIDTH, \
                      paddle1_pos + HALF_PAD_HEIGHT], \
                     PAD_WIDTH, "White")
    
    # draw second paddle
    canvas.draw_line([WIDTH-HALF_PAD_WIDTH, \
                      paddle2_pos - HALF_PAD_HEIGHT], \
                     [WIDTH-HALF_PAD_WIDTH, \
                      paddle2_pos + HALF_PAD_HEIGHT], \
                     PAD_WIDTH, "White")
    
    # determine whether paddle and ball collide
    if ((ball_pos[0] - BALL_RADIUS) <= PAD_WIDTH):
        if (((paddle1_pos + HALF_PAD_HEIGHT) >= \
           ball_pos[1] - BALL_RADIUS / 2) and ((paddle1_pos -\
           HALF_PAD_HEIGHT) <= ball_pos[1] + BALL_RADIUS / 2)):
            
            # Increases the speed and reverse x-direction
            # of the velocity
            ball_vel[0] = -(ball_vel[0] * 1.1)
        else:
            
            # Spawn ball to the right side
            spawn_ball(RIGHT)
            
            # increment score left player
            score2 += 1
    elif ((ball_pos[0] + BALL_RADIUS) >= (WIDTH - PAD_WIDTH)):
        if (((paddle2_pos + HALF_PAD_HEIGHT) >= \
           ball_pos[1] - BALL_RADIUS / 2) and ((paddle2_pos -\
           HALF_PAD_HEIGHT) <= ball_pos[1] + BALL_RADIUS / 2)):
            # Increases the speed and reverse x-direction of the
            # velocity
            ball_vel[0] = -(ball_vel[0] * 1.1)
        else:
            # Spawn ball to the left side
            spawn_ball(LEFT)

            # increment score right player
            score1 += 1

    # collision with top part of screen
    if (ball_pos[1] - BALL_RADIUS) <= 0:
        ball_vel[1] = -ball_vel[1]
    elif (ball_pos[1] + BALL_RADIUS) >= HEIGHT:
        ball_vel[1] = -ball_vel[1]
    
    # draw scores
    canvas.draw_text(str(score1), [ WIDTH / 4, HEIGHT / 8 ],\
                     40, "White")
    canvas.draw_text(str(score2), [ 3 * WIDTH / 4,\
                                   HEIGHT / 8 ], 40, "White")
    
    # Prints message at the beginning of the game or when
    # the game restarts
    if not game_in_progress:
        canvas.draw_text("Press Any Key to Begin!", [\
           3 * WIDTH / 16, HEIGHT / 4], 40, "White")
        
def keydown(key):
    """
    This function is a key down handler.
    """
    
    # Declare global variables
    global paddle1_vel, paddle2_vel, game_in_progress
    
    # Start the game if the game is not in progress
    # Randomize the ball direction at new game
    # 0 is LEFT and 1 is RIGHT
    # else take inputs from the keyboard
    if (game_in_progress == 0):
        game_in_progress = 1
        new_game()
        spawn_ball(random.randrange(0,2))
    else:
        if (key == simplegui.KEY_MAP["down"]):
            paddle2_vel = 5
        elif (key == simplegui.KEY_MAP["up"]):
            paddle2_vel = -5
        elif (key == simplegui.KEY_MAP["w"]):
            paddle1_vel = -5
        elif (key == simplegui.KEY_MAP["s"]):
            paddle1_vel = 5

# Stops the paddle if the key is released
def keyup(key):
    """
    This function is a keyboard handler for
    key up function.
    """
    
    # Declare global variables
    global paddle1_vel, paddle2_vel
    
    # If either "down" or "up" key is released stop the
    # movement of right paddle
    # If either "s" or "w" key is pressed stop the
    # left paddle from moving
    if (key == simplegui.KEY_MAP["down"]) or (key == \
        simplegui.KEY_MAP["up"]):
        paddle2_vel = 0
    elif (key == simplegui.KEY_MAP["s"]) or (key == \
        simplegui.KEY_MAP["w"]):
        paddle1_vel = 0

# Resets the game if the button is pressed
def reset_button():
    """
    This is a helper function that resets the game and call
    the function new game.
    """
    global game_in_progress
    game_in_progress = 0
    new_game()

############################################################
# Create Frame, Draw Handlers, Key up/down handler, buttons


frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", reset_button)

############################################################
# Start Frame


frame.start()
