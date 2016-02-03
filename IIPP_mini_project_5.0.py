# implementation of card game - Memory

import simplegui
import random

# Initialize Cards
cards = range(0,8)
cards = cards.extend(cards)

# This is a class for the game
class Memory(cards):
    def __init__(self, cards):
        self._cards = random.shuffle(cards)
        self._keep = [False] * len(self._cards)
        self._state = 0
        self._turn = 0
        self._last_flip = -1
        self._last_area = -2
        
    def __str__(self):
        """
        Returns the list.
        """
        return self._cards
    
    def get_keep(self, idx):
        """
        Returns the status whether this card is flipped.
        """
        return self._keep[idx]
    
    def change_keep(self, idx):
        """
        Returns the status of whether the card needs to be
        kept flipped open.
        """
        self._keep[idx] = True
    
    def get_card(self, idx):
        """
        Returns the card with given index.
        """
        return self._cards[idx]
    
    def get_cards_list(self):
        """
        Returns list of cards.
        """
        return self._cards
    
    def get_turn(self):
        """
        Returns the number of turns that has passed.
        """
        return self._turn
    
    def increment_turn(self):
        """
        Increase the number of turns.
        """
        self._turn += 1
    
    def change_state_zero(self):
        """
        Change the state of the game to zero.
        """
        self._state = 0
    
    def change_state_one(self):
        """
        Change the state of the game to one.
        """
        self._state = 1
    
    def change_state_two(self):
        """
        Change the state of the game to two.
        """
        self._state = 2
        
    def change_last_flip(self, idx):
        """
        Change the last flipped cards.
        """
        self._last_flip = self._cards[idx]
        
    def get_last_flip(self):
        """
        Get the last flipped cards.
        """
        return self._last_flip
        
    def get_last_area(self):
        """
        Get the last chosen sector.
        """
        return self._last_area
    
    def change_last_area(self, idx):
        """
        Change the last chosen area.
        """
        self._last_area = idx

# helper function to initialize globals
def new_game(memory_game):
    memory_game = Memory
    label.set_text("Turns: " + str(memory_game.get_turn))
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global memory_game
    
    area = pos[0] // 50
    
    # Checks whether the clicked area has been flipped open
    # permanently
    if not memory_game.get_keep(area) and not (memory_game.get_last_area() == area):
        
        # If the state is zero, change the state to 1
        # store the last flipped cards
        if memory_game.get_state() == 0:
            memory_game.change_state_one()
            memory_game.change_last_flip(area)
            memory_game.change_last_area(area)
        elif (memory_game.get_state() == 1):
            if (memory_game.get_last_flip() == memory_game.get_card(area)):
                memory_game.change_keep(area)
                memory_game.change_keep(memory_game.get_last_area())
                memory_game.change_state_two()
            else:
                memory_game.change_state_two()
        else:
            memory_game.change_state_one()
            memory_game.change_last_flip(area)
            memory_game.change_last_area(area)
            memory_game.increment_turns()
    
    # Set the labels
    label.set_text("Turns: " + str(memory_game.get_turn()))
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    n = 0
    global memory_game
    cards = memory_game.get_cards_list()
    
    for card in cards:
        canvas.draw_polygon([[50 * n, 0], \
                             [50 * (n + 1), 0],\
                             [50 * (n + 1), 100],\
                             [50 * n, 100]], 2, 'Yellow',\
                             'Blue')
        n += 1
    for area in range(len(cards)):
        canvas.draw_polygon([[50 * area, 0], \
                             [50 * (area + 1), 0],\
                             [50 * (area + 1), 100],\
                             [50 * area, 100]], 2, 'Yellow',\
                             'Green')
        canvas.draw_text(str(cards[area]),[13 + 50 * area, 65], 50, 'White', 'serif')
    #for area in temp_area:
    #    canvas.draw_polygon([[50 * area, 0], \
    #                         [50 * (area + 1), 0],\
    #                         [50 * (area + 1), 100],\
    #                         [50 * area, 100]], 2, 'Yellow',\
    #                         'Green')
    #    canvas.draw_text(str(memory[area]),[13 + 50 * area, 65], 50, 'White', 'serif')

# create frame and add a button and labels
memory_game = Memory(cards)
frame = simplegui.create_frame("The Memory Game", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game(memory_game)
frame.start()
