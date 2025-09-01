import random
from collections import Counter
cards = list(range(52))

# helper functions
def decode_card(card_number):
    ranks = ["Ace", "2", "3", "4", "5", "6", "7",
                "8", "9", "10", "Jack", "Queen", "King"]
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

    rank = ranks[card_number % 13]
    suit = suits[card_number // 13]
    return f'{rank} of {suit}'

def decode_card_tuple(card_number):
    rank = card_number % 13
    suit = card_number // 13
    return (rank, suit)

def decode_hand(strongest_num):
    hands = ["High Card", "One Pair", "Two Pair", "Three of a kind", "Straight", "Flush", "Full House", "Four of a kind", "Straight Flush"]
    hand = hands[strongest_num]
    return hand

class Player():
    def __init__(self, name, money, hand = None, decoded_hand = None, shared_hand = None, strongest_hand = None):
        self.name = name
        self.money = money
        self.hand = hand if hand is not None else []
        self.decoded_hand = decoded_hand if decoded_hand is not None else []
        self.shared_hand = shared_hand if shared_hand is not None else []
        self.decoded_shared_hand = shared_hand if shared_hand is not None else []
        self.strongest_hand = strongest_hand if strongest_hand is not None else 0

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
        print(self.phase)       
        # guardrails
        if self.phase != 'showdown':
            raise Exception('Not a showdown yet')
        
        # WINNING LOGIC
        
        # show own, shared, community hands
        for player in self.players:
            _temp_list = player.hand + self.upcards
            for card in _temp_list:
                # print string
                decoded = decode_card(card)
                player.decoded_shared_hand.append(decoded)
                # logic tuples
                decoded = decode_card_tuple(card)
                player.shared_hand.append(decoded)
            
            print(f'own hand {player.show_hand()}')
            print(f'shared hand {player.decoded_shared_hand}')
            print(f'logic {player.shared_hand}')
            
            # rank counts 
            ranks = []
            for pair in player.shared_hand:
                ranks.append(pair[0])
            ranks_counts = Counter(ranks)
            print(ranks_counts)

            # suit counts
            suits = []
            for pair in player.shared_hand:
                suits.append(pair[1])
            suits_counts = Counter(suits)
            print(suits_counts)

            # sort ranks
            ranks = list(set(sorted(ranks)))

            # evaluate ranks
            full_house_flag = 0
            two_pair_flag = 0 
            for rank, frequency in ranks_counts.items():
                if frequency == 4:
                    player.strongest_hand = max(player.strongest_hand, )
                elif frequency == 3:
                    if full_house_flag == 1:
                        player.strongest_hand = max(player.strongest_hand, 6)
                    else:
                        full_house_flag += 1
                        player.strongest_hand = max(player.strongest_hand, 3)
                elif frequency == 2:
                    if full_house_flag == 1:
                        player.strongest_hand = max(player.strongest_hand, 6)
                    elif two_pair_flag == 1:
                        player.strongest_hand = max(player.strongest_hand, 2)
                    else:
                        two_pair_flag = 1
                        player.strongest_hand = max(player.strongest_hand, 1)

            # evaluate suits
            for suits, frequency in suits_counts.items():
                if frequency >= 5:
                    player.strongest_hand = max(player.strongest_hand, 5)

            # evaluate sorted ranks
            consecutive_flag = 1
            for i in range(1,len(ranks)):
                if i > 4:
                    if ranks[i] == 0 and ranks[i-1] == 12 and ranks[i-2] == 11 and ranks[i-3] == 10 and ranks[i-4] == 9:
                        player.strongest_hand = max(player.strongest_hand, 4)
                
                diff = ranks[i] - ranks[i-1]
                if diff == 0:
                    continue
                elif diff == 1:
                    consecutive_flag += 1
                else:
                    consecutive_flag = 1
                
                if consecutive_flag == 5:
                    player.strongest_hand = max(player.strongest_hand, 4)

            print(f'Player {player.name} has {player.strongest_hand}')
            decoded = decode_hand(player.strongest_hand)
            print(f'Player {player.name} has {decoded}')


        # show community cards
        print(f'community cards: {self.show_up_cards()}')


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