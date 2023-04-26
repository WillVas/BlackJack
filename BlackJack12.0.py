import random
from time import sleep
import time
import sys
import os


# ---------------------------------------------------------------------------------
# UTILITIES
# Slow print function
def slow_print(string, sleep_time=.075):
    for s in string:
        sys.stdout.write(s)
        sys.stdout.flush()
        time.sleep(sleep_time)


# Clear console function
def clear(set_time):
   sleep(set_time)
   os.system('clear')


# Intro
def intro():
    clear(0)
    slow_print("This is a game of BlackJack...", .1)
    clear(1.25)

    slow_print("Would you like to see the rules? (Y/N): ")
    rules = input().lower()
    if rules == "y":
        clear(.5)
        slow_print("1. All royals are 10\n2. Ace can be 1 or 11 (you choose"
                   ")\n3. Goal is to get up to 21 (Over and you "
                   "lose)\n4. "
                   "Have Fun!", .05)
        clear(2)
    else:
        pass
    slow_print("Ready to start?....")
    clear(1)


# ---------------------------------------------------------------------------------
# GAME MECHANICS
# Create deck
def create_deck():
    deck = []
    for v in open('Python/BJG/CurrentVersion/Deck.csv', encoding="ISO-8859-1"):
        v = v.rstrip("\n")
        line = v.split(",")
        line[0] = int(line[0])
        deck.append(line)
    return deck


# Decides win
def win(house, winner):
    clear(2)
    house.current_dealer_hand()
    winner.current_hand()
    house.balance -= winner.bet
    winner.balance += (winner.bet * 2)
    slow_print("Your winnings are: ")
    print(winner.bet)
    slow_print("Your balance is: ")
    print(winner.balance)
    winner.win_counter += 1
    clear(3)


# Decides loss
def loss(house, looser):
    clear(2)
    house.current_dealer_hand()
    looser.current_hand()
    house.balance += looser.bet
    looser.balance -= looser.bet
    slow_print("You lost: ")
    print(looser.bet)
    slow_print("Your balance is: ")
    print(looser.balance)
    looser.loss_counter += 1
    clear(3)


# Decides tie
def tie(house, tier):
    clear(2)
    house.current_dealer_hand()
    tier.current_hand()
    tier.balance += tier.bet
    slow_print("You tied...")
    slow_print("Your balance is: ")
    print(tier.balance)
    tier.tie_counter += 1
    clear(3)


# Determines if an ace is present in player hand, returns True or False
def ace(player):
    has_ace = False
    for a in player.hand:
        if a[0] == 1:
            has_ace = True
    return has_ace


# Player chooses from 4 possible actions, returns numerical value of said action
def choose(ace_status, player):
    while True:
        try:
            slow_print("\nSelect what you would like to do: ")
            if ace_status:
                if player.double_down:
                    slow_print("\n1. Hit\n2. Stay\n3. Double Down\n4. Change Ace Value\n", .025)
                    option = input()
                    clear(1)
                else:
                    slow_print("\n1. Hit\n2. Stay\n3. Double Down (Unavailable)\n4. Change Ace Value\n", .025)
                    option = input()
            else:
                if player.double_down:
                    slow_print("\n1. Hit\n2. Stay\n3. Double Down\n4. Change Ace Value (Unavailable)\n", .025)
                    option = input()
                else:
                    slow_print("\n1. Hit\n2. Stay\n3. Double Down (Unavailable)\n4. Change Ace Value (Unavailable)\n",
                               .025)
                    option = input()
            clear(1)
            break
        except Exception:
            print("ERROR: NOT AN OPTION")
    return int(option)


# Draw function, returns drawn card
def draw(Deck1, Deck2):
    if len(deck1) > 26:
        card = random.choice(deck1)
        deck1.remove(card)
        deck2.append(card)
        return card
    elif len(deck1) < 26:
        for i in deck2:
            deck1.append(i)
        card = random.choice(deck1)
        deck1.remove(card)
        deck2.append(card)
        return card


# Starts game and draws 2 cards for each person
def start_game(Seats):
    for s in Seats:
        if s.name != "Doug":
            if s.sit_out:
                print(s.name, ": ")
                while True:
                    try:
                        slow_print("Would you like to sit out this turn? (Y/N): ")
                        sitout = input().lower()
                        if sitout == "y":
                            pass
                            break
                        elif sitout == "n":
                            s.sit_out = False
                            clear(1)
                            if len(s.hand) < 2:
                                print(s.name, ": ")
                                slow_print("Press >ENTER< to begin your turn: ")
                                input()
                                clear(1)
                                print(s.name, ": ")
                                s.place_bet()
                                clear(1.25)
                                s.player_hand()
                                s.current_hand()
                                slow_print("Press >ENTER< to end your turn: ")
                                input()
                                clear(.5)
                                s.total()
                                break
                    except Exception:
                        print("ERROR: PLEASE TRY AGAIN")
            else:
                pass
        else:
            if len(s.hand) < 2:
                s.dougs_hand()
            else:
                pass


# ---------------------------------------------------------------------------------
# CLASS
# Table seat class
class Table_Seat:

    def __init__(self, N, H, Bal=10000, Bet=0, T=0, wins=0, loss=0, tie=0, so=True, dd=True, bj=False, bust=False,
                 end=False):
        self.name = N
        self.hand = H
        self.balance = Bal
        self.bet = Bet
        self.hand_total = T
        self.win_counter = wins
        self.loss_counter = loss
        self.tie_counter = tie
        self.sit_out = so
        self.double_down = dd
        self.blackjack = bj
        self.bust = bust
        self.end_turn = end

    # Resets each hand after a round is complete
    def reset(self):
        self.hand = []
        self.bet = 0
        self.hand_total = 0
        self.double_down = True
        self.blackjack = False
        self.bust = False
        self.sit_out = True
        self.end_turn = False

    # Updates the total number a players hand adds to
    def total(self):
        self.hand_total = 0
        for card in self.hand:
            self.hand_total += card[0]

    # Prints player stats
    def current_hand(self):
        print("---------------------------------------------------------------------------------")
        print("Player Stats:")
        print("---------------------------------------------------------------------------------")
        self.total()
        print("Name: ", self.name)
        print("Hand: ", end="")
        for i in self.hand:
            for j in i:
                if j in range(0, 12):
                    pass
                else:
                    print(j, end=", ")
        print()
        print("Total: ", self.hand_total)
        print("Balance: ", self.balance)
        print("Bet: ", self.bet)
        print("---------------------------------------------------------------------------------")

    # Prints dealer stats
    def current_dealer_hand(self):
        print("---------------------------------------------------------------------------------")
        print("Dealer Stats: ")
        print("---------------------------------------------------------------------------------")
        self.total()
        print("Name: ", self.name)
        print("Hand: ", end="")
        print("Hand: ", end="")
        for i in self.hand:
            for j in i:
                if j in range(0, 12):
                    pass
                else:
                    print(j, end=", ")
        print()
        print("Total: ", self.hand_total)
        print("---------------------------------------------------------------------------------")

    # Prompts player to place bet
    def place_bet(self):
        print("Balance: ", self.balance)
        slow_print("How much would you like to bet?: ")
        self.bet = int(input())
        self.balance -= self.bet
        if (self.bet * 2) < self.balance:
            self.double_down = True
        else:
            self.double_down = False

    # Player is given two cards to start the game
    def player_hand(self):
        while len(self.hand) < 2:
            clear(.1)
            self.current_hand()
            slow_print("Press >ENTER< to draw a card")
            input()
            card = draw(deck1, deck2)
            slow_print("You drew a : ")
            print(card[1])
            self.hand.append(card)
            clear(3)

    # Dealer gets two cards to start the game, displays the first
    def dougs_hand(self):
        while len(self.hand) < 1:
            dealer_card = draw(deck1, deck2)
            slow_print("Dealers first card was a: ")
            self.hand.append(dealer_card)
            for i in self.hand:
                print(i[1])
        dealer_card = draw(deck1, deck2)
        self.hand.append(dealer_card)


    # Hit function which draws and displays a card, and adds it to players hand
    def hit(self):
        self.current_hand()
        slow_print("Press >ENTER< to draw a card")
        input()
        self.double_down = False
        card = draw(deck1, deck2)
        slow_print("You drew a: ")
        print(card[1])
        self.hand.append(card)
        clear(1)

    # Allows dealer to draw a card
    def dealer_hit(self):
        slow_print("Doug is hitting...")
        clear(1.5)
        self.current_dealer_hand()
        card = draw(deck1, deck2)
        slow_print("Doug drew a: ")
        print(card[1])
        clear(1.5)
        self.hand.append(card)
        self.total()

    # Allows dealer to change the value of an ace
    def dealer_change_ace(self):
        self.total()
        for Ace in self.hand:
            if Ace[0] == 1:
                slow_print("Doug is changing his ace from 1 to 11")
                Ace[0] = 11
                self.total()
                break
        clear(2)

    # Players bet is doubled, and they are given a single card, turn is ended
    def doubledown(self):
        self.current_hand()
        slow_print("Press >ENTER< to double down and draw a card")
        input()
        clear(1)
        self.balance -= self.bet
        self.bet = self.bet * 2
        card = draw(deck1, deck2)
        self.hand.append(card)
        slow_print("Here are your new stats...")
        clear(1)
        self.current_hand()
        self.double_down = False

    # Player can change ace value as desired
    def change_ace(self):
        self.current_hand()
        for Ace in self.hand:
            if Ace[0] == 1:
                slow_print("Current Value: ")
                print(Ace[0])
                while True:
                    try:
                        slow_print("Change ace to >1< or >11<: ")
                        change = int(input())
                        if change == 1:
                            Ace[0] = change
                            clear(1)
                            slow_print("Your ace is now valued as a 1")
                            break
                        elif change == 11:
                            Ace[0] = change
                            clear(1)
                            slow_print("Your ace is now valued as a 11\n")
                            break
                    except Exception:
                        print("ERROR: NOT POSSIBLE TO CHANGE ACE TO THAT VALUE")
        self.current_hand()


# ---------------------------------------------------------------------------------
# Variables and intro call
intro()
Players = []
dealer_hand = []
deck1 = create_deck()
deck2 = []
start_loop = True
# ---------------------------------------------------------------------------------
# Loop determines number of players and creates and object for each
while True:
    try:
        slow_print("Enter number of players from 1-6: ")
        pn = int(input())
        clear(1)
        if 1 <= pn <= 6:
            if pn >= 1:
                slow_print("Enter a name for player 1: ")
                p1_n = input()
                clear(1)
                bal1 = 100
                crd1 = []
                Table_Seat1 = Table_Seat(p1_n, crd1, bal1)
                Players.append(Table_Seat1)
            if pn >= 2:
                slow_print("Enter a name for player 2: ")
                p2_n = input()
                clear(1)
                bal2 = 100
                crd2 = []
                Table_Seat2 = Table_Seat(p2_n, crd2, bal2)
                Players.append(Table_Seat2)
            if pn >= 3:
                slow_print("Enter a name for player 3: ")
                p3_n = input()
                clear(1)
                bal3 = 100
                crd3 = []
                Table_Seat3 = Table_Seat(p3_n, crd3, bal3)
                Players.append(Table_Seat3)
            if pn >= 4:
                slow_print("Enter a name for player 4: ")
                p4_n = input()
                clear(1)
                bal4 = 100
                crd4 = []
                Table_Seat4 = Table_Seat(p4_n, crd4, bal4)
                Players.append(Table_Seat4)
            if pn >= 5:
                slow_print("Enter a name for player 5: ")
                p5_n = input()
                clear(1)
                bal5 = 100
                crd5 = []
                Table_Seat5 = Table_Seat(p5_n, crd5, bal5)
                Players.append(Table_Seat5)
            if pn >= 6:
                slow_print("Enter a name for player 6: ")
                p6_n = input()
                clear(1)
                bal6 = 100
                crd6 = []
                Table_Seat6 = Table_Seat(p6_n, crd6, bal6)
                Players.append(Table_Seat6)
            Table_Seat7 = Table_Seat("Doug", dealer_hand)
            Players.append(Table_Seat7)
            break
        elif pn < 1:
            print("ERROR: NOT ENOUGH PLAYERS ")
            clear(2)

        elif pn > 6:
            print("ERROR: TOO MANY PLAYERS ")
            clear(2)
    except Exception:
        print("ERROR: PLEASE TRY AGAIN ")
        clear(2)

# ---------------------------------------------------------------------------------
# Main game
while start_loop:

    # Start of game
    start_game(Players)
    # Second turn
    for player in Players:
        # Dealers turn
        if player.name == "Doug":
            slow_print("Dealers turn...")

            while player.hand_total < 17:
                clear(1)
                player.current_dealer_hand()
                dealer_has_ace = ace(player)
                if dealer_has_ace:
                    if 6 <= player.hand_total <= 10:
                        player.dealer_change_ace()
                    else:
                        player.dealer_hit()
                else:
                    player.dealer_hit()

            player.current_dealer_hand()
            if player.hand_total > 21:
                slow_print("Dealer has busted...")
                player.bust = True
            elif player.hand_total == 21:
                slow_print("Dealer has BlackJack...")
                player.blackjack = True
            else:
                slow_print("Dealer has 17..\n")
                slow_print("Doug has ended his turn")
            clear(3)
        # Players turn
        elif player.name != "Doug":
            clear(2)
            for i in Table_Seat7.hand:
                print("Dealers first card was a: ", i[1])
            player.current_hand()
            slow_print("Press >ENTER< to begin your turn: ")
            input()
            clear(1.5)
            while not player.end_turn:
                if player.hand_total > 21:
                    player.bust = True
                    player.end_turn = True

                elif player.hand == 21:
                    player.blackjack = True
                    player.end_turn = True

                elif player.hand_total < 21:
                    for i in Table_Seat7.hand:
                        print("Dealers first card was a: ", i[0])
                    player.current_hand()
                    ace_hand = ace(player)
                    player_choice = choose(ace_hand, player)

                    if player_choice == 1:
                        player.hit()
                        player.total()

                    elif player_choice == 2:
                        slow_print("Stay...\n")
                        player.end_turn = True
                        player.total()

                    elif player_choice == 3:
                        player.doubledown()
                        player.end_turn = True
                        player.total()

                    elif player_choice == 4:
                        player.change_ace()
                        player.total()
            if player.blackjack:
                player.current_hand()
                slow_print("You have a 21...\nBLACKJACK!")

            elif player.bust:
                slow_print("You have a: ")
                print(player.hand_total)
                slow_print("...BUST!\n")
                clear(1.5)
            else:
                slow_print("Your turn has ended...")
                clear(1)
    # Checks for win
    for player in Players:
        player.total()
        if player.name != "Doug":
            if not Table_Seat7.blackjack and not Table_Seat7.bust:

                if Table_Seat7.hand_total < player.hand_total:
                    win(Table_Seat7, player)

                elif Table_Seat7.hand_total > player.hand_total:
                    loss(Table_Seat7, player)

                else:
                    tie(Table_Seat7, player)

            elif Table_Seat7.blackjack:
                if player.blackjack:
                    tie(Table_Seat7, player)

                else:
                    loss(Table_Seat7, player)

            elif Table_Seat7.bust:
                if not player.bust:
                    win(Table_Seat7, player)

                else:
                    tie(Table_Seat7, player)
    # Resets game for multiple rounds
    for reset in Players:
        reset.reset()
    slow_print("Would you like to play again? (Y/N): ")
    restart = input().lower()
    if restart == "n":
        start_loop = False
    else:
        pass
