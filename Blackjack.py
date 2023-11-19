#Happy Blackjacking!

import random
from random import shuffle


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def getvalue(self):
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11
        else:
            return int(self.rank)
        
    def __str__(self):
        return f'{self.rank} of {self.suit}'
    
class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))
        
    def shuffle(self):

        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            print('THE DECK IS EMPTY!')
        
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.hasAce = False

    def addcard(self, card):
        self.cards.append(card)
        card_value = card.getvalue()
        self.value += card_value

        if card.rank == "Ace":
            self.hasAce = True
        self.adjustforace()

    def adjustforace(self):
        while self.value > 21 and self.hasAce:
            self.value -= 10
            self.hasAce = False
            
    def busted(self):
        return self.value > 21
    
    def __str__(self):
        cardlist = ', '.join(str(card) for card in self.cards)
        return f'Hand: {cardlist}\nValue: {self.value}'

    def getvalue(self):
        return self.value
    
    def reset(self):
        self.cards.clear()
        self.value = 0
        self.hasAce = False


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def decision(self):
        while True:
            choice = input(f'{self.name}, do you want to hit or stand?: ').lower().strip()
            if choice in ['hit', 'stand']:
                return choice
            else:
                print('Invalid input. Please choose a valid option')

    def receivecard(self, card):
        self.hand.addcard(card)


class Dealer:
    def __init__(self):
        self.name = 'Dealer'
        self.hand = Hand()

    def dealer_decision(self):
        if self.hand.value < 17:
            return 'hit'
        else:
            return 'stand'

    def dealer_receivecard(self, card):
        self.hand.addcard(card)


class Game:
    def __init__(self, player_name):
        self.deck = Deck()
        self.player = Player(player_name)
        self.dealer = Dealer()

    def startgame(self):
        print("Welcome to the Blackjack Terminal Game!")
        print("The aim of the game is to Hit or Stand, until one of "
              "the players (you and the dealer) either bust or hit 21 points.")
        print('Good Luck!')
        self.deck.shuffle()
        self.newround()

    def newround(self):
        self.player.hand.reset()
        self.dealer.hand.reset()

        for i in range(2):
            self.player.receivecard(self.deck.deal())
            self.dealer.dealer_receivecard(self.deck.deal())

        if self.player.hand.getvalue() == 21 or self.dealer.hand.getvalue() == 21:
            self.checkblackjack()
        self.playerturn()

    def checkblackjack(self):
        if self.player.hand.getvalue() == 21:
            self.endofgame("You have won! Congratulations!")
        elif self.dealer.hand.getvalue() == 21:
            self.endofgame('You Lost!')
        elif self.player.hand.getvalue() == 21 and self.dealer.hand.getvalue() == 21:
            self.endofgame("You tied!")
        else:
            self.playerturn()

    def endofgame(self, outcome):
        print(outcome)
        choice = input('Would you like to play again? (y/n): ').lower().strip()
        if choice == 'y':
            self.newround()
        else:
            print("Thank you for playing, goodbye.")
            exit()

    def playerturn(self):
        while self.player.hand.getvalue() < 21:
            print(f"Your hand: {self.player.hand}")
            decision = self.player.decision()
            if decision == 'hit':
                self.player.receivecard(self.deck.deal())
                print(f"New card added. Your hand is now: {self.player.hand}")
                if self.player.hand.busted():
                    self.endofgame("Busted! You lost!")
                    return
            elif decision == 'stand':
                print(f"You chose to stand. Your final hand: {self.player.hand}")
                break
        self.dealerturn()

    def dealerturn(self):
        while self.dealer.hand.getvalue() < 17:
            self.dealer.dealer_receivecard(self.deck.deal())
            if self.dealer.hand.busted():
                self.endofgame('Dealer busted! You won!')
                return
        self.check_finaloutcome()

    def check_finaloutcome(self):
        playervalue = self.player.hand.getvalue()
        dealervalue = self.dealer.hand.getvalue()

        if playervalue > 21:
            self.endofgame('Busted! You lost!')
        elif dealervalue > 21 or playervalue > dealervalue:
            self.endofgame('You won! Congratulations')
        elif playervalue < dealervalue:
            self.endofgame('The dealer wins.')
        else:
            self.endofgame("You tied!")

if __name__ == "__main__":
    player_name = input("Enter your name: ")
    game = Game(player_name)
    game.startgame()