"""
Class 'De' represents a playing card.

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

from random import choice, choices

import requests

"""
Class 'Dealer' represents the dealer.

    Attributes:
        hand (list): The list of cards in the dealer's hand.
        bankroll (int): The bankroll of the dealer/ house.
        username (str): The username of the dealer.
"""


class Dealer:
    def __init__(self):
        self.hand = []  # hand of the player
        self.bankroll = 0  # bankroll of the house
        self.username = choice(('Pep Guardiola', 'Jürgen Klopp', 'Thomas Tuchel', 'Erik ten Hag'))  # dealers


"""
Class 'Player' represents the base class player.

    Attributes:
        bust (bool): True if the player has busted.
        standing (bool): True if the player is standing.
        hand (list): The list of cards in the player's hand.
        cash (int): The cash of the player.
        first (bool): True if it is player's first round.
        split (bool): True if the player has split.
        bet (int): The bet of the player.
        insurance (int): The insurance of the player.

"""


class Player:
    def __init__(self, parent=None):
        self.bust = False  # bust or not
        self.standing = False  # standing or not
        self.hand = []  # hand of the player
        self.cash = 1000  # bankroll of the player
        # first round decides whether the player is eligible to surrender/ double down/ split
        self.first = True
        self.split = False
        self.bet = 0
        self.insurance = 0


"""
Class 'Computer' represents the 'player' managed by computer.

    Attributes:
        all attributes of the class 'Player'
        username (str): The username of the computer.
        engine (Engine): The engine of the computer.
"""


class Computer(Player):
    def __init__(self, engine):
        super().__init__()

        # create a random username using api
        data = requests.get('https://randomuser.me/api').json()
        self.username = data['results'][0]['login']['username']

        # creating an instance of the parameter engine class
        self.engine = engine(self)
        print(self.engine.documentation)


"""
Class 'Atharva' represents the novice engine.

    Attributes:
        documentation (str): The documentation of the engine.
        entity (str): The entity managed by the engine.
    
    Methods:
        play (): The method to play a round. Returns the appropriate function (hit/stand ...).
        place_bet (): The method to place appropriate bet.
        buy_insurance (): The method to buy insurance. Returns a bool value.
"""


class Atharva:
    def __init__(self, entity):
        self.documentation = f'{entity.username} is a managed by engine Atharva'
        self.entity = entity

    def play(self):
        if calculate_hand(self.entity.hand) < 17:
            return hit
        else:
            return stand

    def place_bet(self):
        if self.entity.cash >= 100:
            return 100
        else:
            return self.entity.cash

    @staticmethod
    def buy_insurance():
        # parameter k is the number of items to return
        # parameter weights is a list of weights for each item
        return choices([True, False], weights=[3, 8], k=1)[0]  # P(True) = 3/11


"""
Class 'Rangnick' represents the intermediate engine.
Decisions are made by the engine based on the basic strategy of the blackjack.
* requires a global variable 'upcard' to be defined, which is the value of the dealer's upcard.

    Attributes:
        documentation (str): The documentation of the engine.
        entity (str): The entity managed by the engine.

    Methods:
        play (): The method to play a round. Returns the appropriate function (hit/stand ...).
        place_bet (): The method to place appropriate bet.
        buy_insurance (): The method to buy insurance. Returns a bool value.
"""


class Rangnick:
    def __init__(self, entity):
        self.documentation = f'{entity.username} is a managed by engine Ralf Rangnick'
        self.entity = entity

    def play(self):  # gameplay based on basic strategy
        global upcard  # to be defined globally in the driver function
        hand_total = calculate_hand(self.entity.hand)

        is_soft = check_soft(self.entity.hand)
        is_first = self.entity.first

        if is_soft:
            if 20 == hand_total:  # Soft 20 (A,9) always stands.
                return stand

            if 19 == hand_total:  # Soft 19 (A,8) doubles against dealer 6, otherwise stand.
                if upcard.value == 6 and self.entity.first:
                    return double_down
                else:
                    return stand

            # Soft 18 (A,7) doubles against dealer 2 through 6, and hits against 9 through Ace, otherwise stand.
            if 18 == hand_total:
                if upcard.value in [2, 3, 4, 5, 6]:
                    if self.entity.first:
                        return double_down
                    else:
                        return stand

                elif upcard.value in [7.8]:
                    return hit

                elif upcard.rank in ['9', '10', 'J', 'Q', 'K', 'A']:
                    return hit

        # surrender
        if (16 == hand_total) and (upcard.value in [9, 10, 1]) and is_first:
            return surrender

        if (15 == hand_total) and (upcard.value in [10]) and is_first:
            return surrender

        # hard hand
        if 17 <= hand_total:
            return stand

        if hand_total in [16, 15, 14, 13]:
            if upcard.value in [2, 3, 4, 5, 6]:
                return stand
            else:
                return hit

        if 12 == hand_total:
            if upcard.value in [4, 5, 6]:
                return stand
            else:
                return hit

        if 11 == hand_total:
            if is_first:
                return double_down
            else:
                return hit

        if 10 == hand_total:
            if upcard.value in [2, 3, 4, 5, 6, 7, 8] and is_first:
                return double_down
            else:
                return hit

        if 9 == hand_total:
            if upcard.value in [3, 4, 5, 6] and is_first:
                return double_down
            else:
                return hit

        if 8 >= hand_total:
            return hit

    def place_bet(self):
        if self.entity.cash >= 100:
            return 100
        else:
            return self.entity.cash

    @staticmethod
    def buy_insurance():
        return 'no'


# Hand Analysis functions.
def calculate_hand(hand):  # calculate the best value for the hand
    total = 0
    ace_count = 0

    for card in hand:
        total += card.value
        if card.value == 1:
            ace_count += 1

    # consider ace as 11 till hand stays below 21
    while total + 10 <= 21 and ace_count > 0:
        ace_count -= 1
        total += 10

    return total


def check_soft(hand):  # check if a hand is a soft hand
    for cards in hand:
        if cards.rank == 'A':
            return True
    return False


# Command functions
def hit(player):
    global playing_shoe  # to be defined globally in the driver function
    player.first = False

    hit_card = playing_shoe.draw_card()
    player.hand.append(hit_card)
    #  play hit sound...
    print(f'+ {hit_card.symbol}')

    hand_total = calculate_hand(player.hand)

    if hand_total > 21:  # bust
        player.bust = True
        player.standing = False  # hand not to be considered for further actions
        dealer.bankroll += player.bet
        print(f'Bust!, hand value: {hand_total}')
        print(f'{player.username} loses {player.bet}')
        return False

    if hand_total == 21:
        player.stand = True
        print(f'Hand value: 21')
        return False  # no need to ask for hit again, cannot play further

    return True  # signifies that the player can play further


def stand(player):
    player.standing = True
    print(f'{player.username} stands')

    return False  # signifies that the player cannot play further


def surrender(player):
    global dealer  # to be defined globally in the driver function
    if not player.first:
        print(f'Hand cannot be surrendered after the first round')
        return True  # signifies that the player can play further

    # Half of the bet is lost
    player.cash += int(player.bet / 2)  # the other half is returned to the player
    dealer.bankroll += int(player.bet / 2)  # the other half is taken by the dealer
    player.status = False
    player.stand = False  # hand not to be considered for further actions
    print('Hand surrendered')

    # signifies that the player cannot play further
    return False


def split(player):
    pass


def double_down(player):
    if not player.first:
        print(f'Cannot double down after the first round')
        return True  # signifies that the player can play further

    if player.cash < player.bet:
        print('Not enough cash to double down')
        return True  # signifies that the player can play further

    player.first = False

    player.bet *= 2  # double the bet
    print(f'Bet doubled to {player.bet}')

    player.stand = True  # hand to be considered for further actions
    hit(player)
    return False  # signifies that the player cannot play further
