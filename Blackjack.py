import random
from time import sleep

import requests

from Cards import Shoe

print('Elon Musk')


def game():
    index = 0
    names = ['Gregory House', 'Lisa Cuddy', 'James Wilson', 'Allison Cameron', 'Robert Chase', 'Eric Foreman']



    '''class Colin:
        def __init__(self, entity):
            self.documentation = f'{entity.username} is a managed by engine Colin Jones'
            self.entity = entity'''

    # derived class User
    class User(Player):
        def __init__(self):
            self.cash = 1000  # bankroll of the player

            nonlocal index
            super().__init__()
            self.username = names[index]
            index += 1





    # function accessed within the function print_hand function
    def _print_cards(hand):
        for card in hand:
            print(card.symbol, end=' ')

    def print_hand():
        print(f"{player.username}: ", end='')

        # split hand
        if isinstance(player.hand[0], list):
            for hand_i in player.hand:
                _print_cards(hand_i)

        # single hand
        else:
            _print_cards(player.hand)

    # resetting the status of players on the table
    def reset_table():
        playing_shoe.shuffle()  # refilling the shoe

        #  resetting the status of players on the table
        for player_i in table:
            player_i.hand = []
            player_i.status = True
            player_i.stand = False
            player_i.hand.clear()
            player_i.first = True
            player_i.split = False
            player_i.parent = player_i
            player_i.bet = 0
            player_i.insurance = 0

        # resetting the hand of dealer
        dealer.hand = []



    def validate_insurance():
        for player_i in table:
            if facedown.rank == '10':
                print(f'Insurance won, {player_i.username} won 2*{player_i.insurance} = {2 * player_i.insurance}')
                player_i.cash += 2 * player_i.insurance
                dealer.bankroll -= player_i.insurance

            else:
                print(f'Insurance lost, {player_i.username} lost {player_i.insurance}')
                dealer.bankroll += player_i.insurance

    # global object of class shoe
    playing_shoe = Shoe()

    print('Welcome Screen')

    # input of number of bots & users
    # bots = min(int(input('Number of bots: ')), 4)
    # users = min(int(input('Number of users: ')), 3)
    bots = 2
    users = 3

    dealer = Dealer()
    table = []

    # adding bots to the table
    for _ in range(bots):
        table.append(Computer(engine=Atharva))

    table.append(Computer(engine=Rangnick))
    table.append(Computer(engine=Rangnick))

    # adding users to the table
    for i in range(users):
        # print(f'Enter a username for Player {i}: ', end='')
        table.append(User())

    # displaying players on the table
    print('\n\n\t------ TABLE ------')
    print(f'\t* {dealer.username} (Dealer)')
    for i in table:
        if isinstance(i, Computer):
            print(f'\t{i.username} (bot)')

        else:  # player is a user
            print(f'\t{i.username} (user)')

    print('\n\n')

    # viable commands
    commands = {'hit': hit, 'stand': stand, 'surrender': surrender, 'double down': double_down, 'split': split}

    # Game loop
    while True:
        print('Setting up the table...')
        reset_table()  # resets the table & shoe
        # sleep(2)

        upcard = None
        facedown = None

        # players place bets
        for player in table:
            if isinstance(player, User):
                # player.bet = int(input(f'{player.username}, place your bet: '))
                player.bet = 100

            elif isinstance(player, Computer):
                player.bet = player.engine.place_bet()
                # sleep(0.5)

            player.cash -= player.bet
            print(f'{player.username} bets {player.bet}')

        print('\nDealing cards..')
        # dealing cards to players
        for _ in range(0, 2):
            for player in table:
                player.hand.append(playing_shoe.draw_card())
                # print(f'{player.username}: {player.hand[-1].symbol}') # for debugging
                # sleep(0.8)

        facedown = playing_shoe.draw_card()
        upcard = playing_shoe.draw_card()

        dealer.hand = [facedown, upcard]

        print(f"\n** Dealer's upcard: {upcard.symbol}\n")
        sleep(2)

        # displaying cards of players & checking for blackjack
        for player in table:
            print_hand()
            #  checking for blackjack
            if calculate_hand(player.hand) == 21:
                player.bust = True  # hand not to be considered for evaluation
                print(f': BLACKJACK!, {player.username} wins ${player.bet * 1.5}\n')
                player.cash += player.bet * 1.5
                dealer.bankroll -= player.bet * 0.5
                continue
            print('\n')

        #  Asking for insurance / player.engine.buy_insurance()
        if upcard.rank == 'A':
            for player in table:
                if isinstance(player, User):
                    if (input(f'{player.username}, do you want to buy insurance? (y/n)') + ' ').lower()[0] == 'y':
                        # player buys insurance
                        player.insurance = player.bet
                        #  check for sufficient funds
                        print(f'{player.username} bought insurance for {player.insurance}')

                elif isinstance(player, Computer):
                    player.engine.buy_insurance()

                player.cash -= player.insurance  # default insurance is 0

            #  validating the insurance
            validate_insurance()

        for player in table:
            if player.bust:
                continue

            print(f'Upcard: {upcard.symbol}')

            while True:
                print_hand()
                print(f': {calculate_hand(player.hand)}')
                # if player is a bot
                if isinstance(player, Computer):
                    # print(f'{player.username} is thinking...')
                    sleep(2)
                    player.action = player.engine.play()
                    print(f'{player.username} chose {player.action.__name__}| ', end='')

                # if player is a user
                else:
                    player.action = commands.get(input('Command: ').lower(), lambda: -1)

                outcome = player.action()

                if outcome == -1:
                    print('Invalid command')
                    continue

                if not outcome:  # bust/ stand
                    print('\n')
                    break

        # dealer's turn, hits till 17
        player = dealer
        print(f'Dealer hits till 17')
        print_hand()
        while calculate_hand(player.hand) < 17:
            hit()

        print_hand()
        print(f': {calculate_hand(player.hand)}')
        dealers_hand = calculate_hand(player.hand)  # player variable is the dealer

        # if dealer busts
        if dealers_hand > 21:
            print(f'Dealer busts!, {print_hand()}: {calculate_hand(player.hand)}')
            for player in table:
                if player.bust or isinstance(player, Dealer):
                    continue
                player.cash += 2 * player.bet
                dealer.bankroll -= player.bet
                print(f'{player.username} won ${player.bet}! : ({calculate_hand(player.hand)})')

        # table is evaluated wins/losses/push
        else:
            for player in table:
                if isinstance(player, Dealer) or player.bust:
                    continue

                player_hand = calculate_hand(player.hand)  # calculating the player's hand value
                # player wins
                if player_hand > dealers_hand:
                    player.cash += player.bet * 2
                    dealer.bankroll -= player.bet
                    print(f'{player.username} won ${player.bet}! : ({player_hand})')
                    sleep(1)

                # dealer wins
                elif player_hand < dealers_hand:
                    dealer.bankroll += player.bet
                    print(f'{player.username} lost ${player.bet} : ({player_hand})')
                    sleep(1)

                # push
                else:
                    player.cash += player.bet
                    print(f'{player.username} pushed! : ({player_hand})')
                    sleep(1)

        # if player has cash left, he can play again
        for player in table:
            if player.cash > 0:
                print(f'{player.username} has {player.cash} left')
                break
            else:
                print(f'{player.username} has no more cash left')
                table.remove(player)

        # if player wants to cash out
        for player in table:
            if isinstance(player, User):
                if input(f'{player.username}, Cash out with ${player.cash} ?: ').lower() == 'y':
                    print(f'{player.username} has left the table with a gain of ${player.cash - 1000}')
                    table.remove(player)

        # if there are no players left, the game ends
        if len(table) == 0:
            print('Game Over')
            return dealer

        print('>> New Round')
        sleep(5)


if __name__ == '__main__':
    game()  # |>
