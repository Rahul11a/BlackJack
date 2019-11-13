import random
'''
These are global variables representing the deck
'''
suits = ('Heart', 'Spade', 'Diamond', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2 , 'Three': 3 , 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
playing = True

'''
This Class right here stores the characteristics of a card
A Suit and a Rank is what we need
'''
class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        ## This will be stored in the deck list
        return self.rank + " of " + self.suit

'''
This class represent all the 52 cards
'''
class Deck():
    def __init__(self):
        self.deck = [] # Empty deck
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
                ## Now one element of this string represents "rank of suit"

    '''
    __str__ can only return string. 
    Hence to return a list use a for loop
    '''
    def __str__(self):
        deck_assembly = ''
        for card in self.deck:
            deck_assembly += '\n' + card.__str__()
        return "The Deck has: "+deck_assembly
    def shuffle(self):
        random.shuffle(self.deck)
    def deal(self):
        ## .pop() function gets you the popped card
        single_card = self.deck.pop()
        return single_card

class Hand:
    def __init__(self):
        self.card = []
        #total sum of the value of the cards
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        # Card passed in is from the deck and returned
        # Deal function
        self.card.append(card)
        self.value += values[card.rank]
        '''
        Here card = self.rank of self.suit
        And we are looking for the rank part to call the value from the 'values' dict
        Hence card.value
        '''

        # Check for Aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        # If total value > 21 AND there are still aces left
        # Than change the value of ace to 1
        while self.value > 21 and self.aces:
            self.value -=10
            self.aces -= 1

class Chips():
    def __init__(self, total = 100):
        self.total = total # default value of total
        self.bet = 0 # default

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except ValueError:
            print("Sorry please provide and integer")
            continue
        else:
            if chips.bet > chips.total:
                print(f"Sorry, you do not have enough chips!. you have: {chips.total}")
            else:
                break
'''
This function takes in two attributes 
These represents the variables which will be later pointed to these classes
As we are using the methods of these classes
'''
def hit(deck,hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()
def hit_or_stand(deck,hand):
    global playing # to control an upcoming while loop
    while True:
        X = input('Hit or Stand? Enter H or S ').upper()
        if X[0] == 'H':
            hit(deck, hand)
        elif X[0] == 'S':
            print("Player Stands Dealer's Turn")
            playing = False
        else:
            print("Sorry I did not understand that, Please enter h or s only!")
            continue
        break
def show_some(player,dealer):
    print('DEALERS HAND: ')
    print('one card hidden!')
    print(dealer.card[1])
    print('\n')
    print('PLAYER HAND: ')
    for card in player.card:
        print(card)
def show_all(player,dealer):
    print('DEALERS HAND: ')
    for card in dealer.card:
        print(card)
    print('\n')
    print('PLAYER HAND: ')
    for card in player.card:
        print(card)


def player_busts(player, dealer, chips):
    print("PLAYER BUSTED!")
    chips.lose_bet()
def player_wins(player, dealer, chips):
    print("PLAYER WON")
    chips.win_bet()
def dealer_busts(player, dealer, chips):
    print("PLAYER WINS, DEALER BUSTED")
    chips.win_bet()
def dealer_wins(player, dealer, chips):
    print("DEALER WINS")
    chips.lose_bet()
def push(player, dealer):
    print("Dealer and the player tie! PUSH")


'''
Driver Function
'''
balance = 100
while True:
    '''
    Starting the game
    Setting up player's hand and dealer's hand
    '''
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    ## Set the player's chips
    player_chips = Chips(total = balance)

    ## Asking the player to bet
    take_bet(player_chips)

    ## Show cards
    show_some(player_hand, dealer_hand)

    while playing:
        ## Asking the player to choose between hitting or standing
        hit_or_stand(deck, player_hand)

        ## Show cards
        show_some(player_hand, dealer_hand)

        '''
        Now running conditions on winning and busting
        '''
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
    if player_hand.value < 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all the cards
        show_all(player_hand, dealer_hand)

        # More winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)


    # Inform the player about the chips
    balance = player_chips.total
    print('\n Total chips left: {}'.format(player_chips.total))

    # Asking the player if they want another hand
    new_game = input("Do you want to play another hand? Y/N").upper()
    if new_game == 'Y':
        playing = True
        continue
    else:
        print("Thank you for playing!!")
        break
