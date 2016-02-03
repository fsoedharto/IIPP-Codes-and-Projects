##########################################################
# Mini-project #6 - Blackjack


import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

##########################################################
# Define Classes


# define card class
class Card:
    """
    This class is for the cards which includes the ranks,
    suits, and drawing the cards.
    """
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        """
        Prints rank and suit in readable form.
        """
        return self.suit + self.rank

    def get_suit(self):
        """
        Return the suit of the card.
        """
        return self.suit

    def get_rank(self):
        """
        Return the rank of the cards.
        """
        return self.rank

    def draw(self, canvas, pos):
        """
        Draw the cards.
        """
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    """
    This is the class for the hand.
    """
    def __init__(self):
        self.card_list = []

    def __str__(self):
        """
        Return a string representation of a hand.
        """
        string = 'Hand Contains: '
        for cards in self.card_list:
            if (cards.get_suit() == 'S'):
                string = string + 'S'
            elif (cards.get_suit() == 'C'):
                string = string + 'C'
            elif (cards.get_suit() == 'D'):
                string = string + 'D'
            else:
                string = string + 'H'
            if (cards.get_rank() == 'A'):
                string = string + 'A '     
            elif (cards.get_rank() == 'K'):
                string = string + 'K '
            elif (cards.get_rank() == 'Q'):
                string = string + 'Q '
            elif (cards.get_rank() == 'J'):
                string = string + 'J '
            else:
                string = string + str(cards.get_rank()) + ' '
        return string
    
    def add_card(self, card):
        """
        Add a card object to a hand.
        """
        self.card_list.append(card)

    def get_value(self):
        """
        Count aces as 1, if the hand has an ace, 
        then add 10 to hand value if it doesn't bust
        compute the value of the hand, see Blackjack video
        """
        
        hand_value = 0
        card_rank = []
        
        # Reiterates over the card list
        for cards in self.card_list:
            hand_value += int(VALUES[cards.get_rank()])
            card_rank.append(cards.get_rank())
        if ("A" in card_rank) and ((hand_value + 10) <= 21):
                hand_value += 10
        return hand_value
   
    def draw(self, canvas, pos):
        n = 0
        """
        Draw a hand on the canvas, use the draw method 
        for cards.
        """
        for cards in self.card_list:
            cards.draw(canvas, pos)
            pos[0] += 73
        
# define deck class 
class Deck:
    """
    This class is for the deck class.
    """
    def __init__(self):
    # create a Deck object
        self.deck = []
        i = 0
        while i < len(SUITS):
            j = 0
            while j < len(RANKS):
                self.deck.append(Card(SUITS[i], RANKS[j]))
                j += 1
            i += 1

    def shuffle(self):
        """
        Shuffle the deck use random.shuffle()
        """
        return random.shuffle(self.deck)

    def deal_card(self):
        """
        Deal a card object from the deck
        """
        return self.deck.pop(0)
    
    def __str__(self):
        """
        Prints the string of the deck.
        """
        string = 'Deck Contains: '
        for cards in self.deck:
            if (cards.get_suit() == 'S'):
                string = string + 'S'
            elif (cards.get_suit() == 'C'):
                string = string + 'C'
            elif (cards.get_suit() == 'D'):
                string = string + 'D'
            else:
                string = string + 'H'
            if (cards.get_rank() == 'A'):
                string = string + 'A '     
            elif (cards.get_rank() == 'K'):
                string = string + 'K '
            elif (cards.get_rank() == 'Q'):
                string = string + 'Q '
            elif (cards.get_rank() == 'J'):
                string = string + 'J '
            else:
                string = string + str(cards.get_rank()) + ' '
        return string

###########################################################
# Define event handlers for buttons

# Button Handlers for dealing the card
def deal():
    """
    Initialize variables for Deck and computer hand and
    shuffles the deck.
    """
    global outcome, in_play, hand_player, hand_comp, deck, score
    
    deck = Deck()
    deck.shuffle()
    hand_player = Hand()
    hand_comp = Hand()
    outcome = "Hit or stand?"
    
    # Subtract score if deal button is clicked mid-play
    if in_play:
        score -= 1
    
    # Deal two cards to player
    hand_player.add_card(deck.deal_card())
    hand_player.add_card(deck.deal_card())
    
    # Deal two cards to computer or dealer
    hand_comp.add_card(deck.deal_card())
    hand_comp.add_card(deck.deal_card())

    # A flag for whether the game is busted
    in_play = True

def hit():
    """
    Button handler for drawing cards from the deck. Check
    If the player bust upon drawing the cards.
    """
    global outcome, in_play, score, hand_player, deck
 
    # if the hand is in play, hit the player
    if in_play:
        hand_player.add_card(deck.deal_card())

    # if busted, assign a message to outcome, update in_play and score
        if (hand_player.get_value() > 21):
            in_play = False
            outcome = "You have busted! New Deal?"
            score -= 1
    
def stand():
    """
    Button handler to not draw anymore cards from the Deck. Checks if
    the computer hand is below 17 which will then be bust.
    """
    global outcome, in_play, score, hand_comp, deck
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while hand_comp.get_value() < 17:
            hand_comp.add_card(deck.deal_card())
        
        # assign a message to outcome, update in_play and score
        if (hand_comp.get_value() > 21):
            in_play = False
            outcome = "Dealer Busted! New Deal?"
            score += 1
        elif (hand_player.get_value() > hand_comp.get_value()):
            in_play = False
            outcome = "You Win! New Deal?"
            score += 1
        elif (hand_player.get_value() < hand_comp.get_value()):
            in_play = False
            outcome = "Dealer Wins! New Deal?"
            score -= 1
        else:
            in_play = False
            outcome = "It's a Tie! Dealer Wins! New Deal?"
            score -= 1

# draw handler    
def draw(canvas):
    """
    This is the draw handler for the cards.
    """
    # Draw the player's hands
    hand_player.draw(canvas, [150, 350])
    
    # Draw the dealer's hands
    hand_comp.draw(canvas, [150, 125])
    
    # Cover the dealer's card if in play
    if in_play:
        canvas.draw_image(card_back, [CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]], CARD_SIZE, [150 + CARD_CENTER[0], 125 + CARD_CENTER[1]], CARD_SIZE)
    
    # Draws the result text and score
    canvas.draw_text(outcome, [50, 300], 30, 'White')
    canvas.draw_text("Score: " + str(score), [400, 75], 40, 'White')
    canvas.draw_text("Blackjack", [50, 75], 40, 'White')
    canvas.draw_text("Dealer", [30, 180], 40, 'Yellow')
    canvas.draw_text("Player", [30, 405], 40, 'Yellow')

###########################################################
# Initialization frame


frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

###########################################################
# Create buttons and set draw handler


frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

###########################################################
# Start the game


deal()
frame.start()
