"""
Class 'Card' represents a playing card.

    Attributes:
        suit (str): The suit of the card ♣/♦/♥/♠.
        rank (str): The rank of the card A/2/3/4/5/6/7/8/9/10/J/Q/K.
        symbol (str): The symbol of the card to be shown to the user (♠A, ♥7 ...).
        value (int): The value of the card A = 1/11 Face-cards = 10.
        logo (str): The logo of the card (🂠, 🂡, 🂢, 🂣, 🂤, 🂥, 🂦, 🂧, 🂨, 🂩 ...).

Class 'Shoe' represents a shoe of cards.

    Attributes:
        deck (list): The list of cards in the shoe.

"""

from random import shuffle


class Card:
    def __init__(self, suit, rank):
        self.suit = suit  # ♣/♦/♥/♠
        self.rank = rank  # A/2/3/4/5/6/7/8/9/10/J/Q/K
        self.symbol = suit + rank
        self.logo = '🂠'

        # setting value of ace card
        if self.rank == 'A':
            self.value = 1

        # setting value of face cards
        elif self.rank in ['J', 'Q', 'K']:
            self.value = 10

        # setting the value of the remaining cards
        else:
            self.value = int(rank)


class Shoe:
    shoe_deck = []
    # deck of cards
    deck = [Card(suit, rank) for suit in ['♣', '♦', '♥', '♠'] for rank in
            ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']]

    def __init__(self, num_decks=1):
        self.num_decks = num_decks  # number of decks in the shoe
        for _ in range(min(num_decks, 8)):
            self.shoe_deck.extend(self.deck)

        self.shuffle()

    def shuffle(self):
        # refill the shoe
        self.__init__(self.num_decks)

        # shuffle the list 'deck'
        shuffle(self.shoe_deck)

    def draw_card(self):
        return self.shoe_deck.pop()
