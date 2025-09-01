import random
cards = list(range(52))

# helper functions
def decode_card(card_number):
    ranks = ["Ace", "2", "3", "4", "5", "6", "7",
                "8", "9", "10", "Jack", "Queen", "King"]
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

    rank = ranks[card_number % 13]
    suit = suits[card_number // 13]
    return f'{rank} of {suit}'

class Player():
    def __init__(self, name, money, hand = None, decoded_hand = None):
        self.name = name
        self.money = money
        self.hand = hand if hand is not None else []
        self.decoded_hand = decoded_hand if decoded_hand is not None else []
    
    def show_hand(self):
        return f'{self.name} has {self.decoded_hand}'

class Table():
    def __init__(self, players, pot = None, upcards = None, deck = None, phase='preflop', burn = None, decoded_upcards = None):
        self.players = players
        self.pot = pot if pot is not None else 0
        self.upcards = upcards if upcards is not None else []
        self.decoded_upcards = decoded_upcards if decoded_upcards is not None else []
        self.deck = deck if deck is not None else cards.copy()
        self.phase = phase
        self.burn = burn if burn is not None else []

    def show_up_cards(self):
        return f'{self.decoded_upcards}'

    def start(self):
        self.preflop()
        self.flop()
        self.turn()
        self.river()
        self.showdown()

    def preflop(self):
        print(self.phase)       
        # shuffle the deck
        random.shuffle(self.deck)
        
        # give each player 2 cards
        for _ in range(2):
            for player in self.players:
                card = self.deck.pop()
                player.hand.append(card)
                decoded = decode_card(card)
                player.decoded_hand.append(decoded)
    
        # show cards for each player:
        for player in self.players:
            print(player.show_hand())
        
        # update phase STAGE ENDS
        self.phase = 'flop'
    
    def flop(self):
        print(self.phase)       
        # guardrails
        if self.phase != 'flop':
            raise Exception('Not a flop yet')

        # burn a card
        card = self.deck.pop()
        self.burn.append(card)
        
        # give 3 cards in the middle
        for _ in range(3):
            card = self.deck.pop()
            self.upcards.append(card)
            decoded = decode_card(card)
            self.decoded_upcards.append(decoded)
        
        # show cards for each player:
        for player in self.players:
            print(player.show_hand())
        
        # show the upcards
        print(self.show_up_cards())
        
        # update phase STAGE ENDS
        self.phase = 'turn'

    def turn(self):
        print(self.phase)       
        # guardrails
        if self.phase != 'turn':
            raise Exception('Not a turn yet')
        # burn a card
        card = self.deck.pop()
        self.burn.append(card)
        
        # give 1 card in the middle
        card = self.deck.pop()
        self.upcards.append(card)
        decoded = decode_card(card)
        self.decoded_upcards.append(decoded)

        # show cards for each player:
        for player in self.players:
            print(player.show_hand())

        # show the upcards
        print(self.show_up_cards())

        # update phase STAGE ENDS
        self.phase = 'river'
    
    def river(self):
        print(self.phase)       
        # guardrails
        if self.phase != 'river':
            raise Exception('Not a river yet')
        # burn a card
        card = self.deck.pop()
        self.burn.append(card)
        
        # give 1 card in the middle
        card = self.deck.pop()
        self.upcards.append(card)
        decoded = decode_card(card)
        self.decoded_upcards.append(decoded)

        # show cards for each player:
        for player in self.players:
            print(player.show_hand())

        # show the upcards
        print(self.show_up_cards())

        # update phase STAGE ENDS
        self.phase = 'showdown'
    
    def showdown(self):
        # guardrails
        if self.phase != 'showdown':
            raise Exception('Not a showdown yet')
        
        # TODO WINNING LOGIC
        # show the upcards and players cards
        for player in self.players:
            print(player.show_hand())
        print(self.show_up_cards())

        


        # TODO MONEY TRANSFERS

        # reset everything
        self.burn = []
        for player in self.players:
            player.hand = []
            player.decoded_hand = []
        self.deck = cards.copy()
        random.shuffle(self.deck)
        self.upcards = []
        self.decoded_upcards = []


p1 = Player('A', 100)
p2 = Player('B', 100)
p3 = Player('C', 100)

players = [p1, p2, p3]
game_table = Table(players)
game_table.start()