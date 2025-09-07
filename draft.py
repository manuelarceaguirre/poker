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

def evaluate_hand(shared_hand):
    strongest_hand = 0
    
    # rank counts 
    ranks = []
    for pair in shared_hand:
        ranks.append(pair[0])
    ranks_counts = Counter(ranks)

    # suit counts
    suits = []
    for pair in shared_hand:
        suits.append(pair[1])
    suits_counts = Counter(suits)

    # sort ranks
    ranks = list(set(sorted(ranks)))

    # evaluate ranks
    full_house_flag = 0
    two_pair_flag = 0 
    for rank, frequency in ranks_counts.items():
        if frequency == 4:
            strongest_hand = max(strongest_hand, 7)
        elif frequency == 3:
            if full_house_flag == 1:
                strongest_hand = max(strongest_hand, 6)
            else:
                full_house_flag += 1
                strongest_hand = max(strongest_hand, 3)
        elif frequency == 2:
            if full_house_flag == 1:
                strongest_hand = max(strongest_hand, 6)
            elif two_pair_flag == 1:
                strongest_hand = max(strongest_hand, 2)
            else:
                two_pair_flag = 1
                strongest_hand = max(strongest_hand, 1)

    # evaluate suits
    for suit, frequency in suits_counts.items():
        if frequency >= 5:
            # collect the ranks of this suit
            flush_cards = [r for (r,s) in shared_hand if s == suit]
            flush_cards = sorted(set(flush_cards))
            # check if the ranks form a straight
            consecutive_flag = 1
            for i in range(1, len(flush_cards)):
                if flush_cards[i] - flush_cards[i-1] == 1:
                    consecutive_flag += 1
                elif flush_cards[i] != flush_cards[i-1]:
                    consecutive_flag = 1
                if consecutive_flag == 5:
                    strongest_hand = max(strongest_hand, 8)
            # if no straight found, at least a flush
            if strongest_hand < 8:
                strongest_hand = max(strongest_hand, 5)

    # evaluate sorted ranks
    consecutive_flag = 1
    for i in range(1,len(ranks)):
        if i > 4:
            if set([0, 9, 10, 11, 12]).issubset(ranks):
                strongest_hand = max(strongest_hand, 4)
        
        diff = ranks[i] - ranks[i-1]
        if diff == 0:
            continue
        elif diff == 1:
            consecutive_flag += 1
        else:
            consecutive_flag = 1
        
        if consecutive_flag == 5:
            strongest_hand = max(strongest_hand, 4)
        
    return strongest_hand

def reset_everything():
    self.burn = []
    for player in self.players:
        player.hand = []
        player.decoded_hand = []
    self.deck = cards.copy()
    random.shuffle(self.deck)
    self.upcards = []
    self.decoded_upcards = []
    

class Player():
    def __init__(self, name, money, folded = None, hand = None, decoded_hand = None, shared_hand = None, decoded_shared_hand = None, strongest_hand = None):
        self.name = name
        self.money = money
        self.hand = hand if hand is not None else []
        self.decoded_hand = decoded_hand if decoded_hand is not None else []
        self.shared_hand = shared_hand if shared_hand is not None else []
        self.decoded_shared_hand = [] 
        self.strongest_hand = strongest_hand if strongest_hand is not None else 0
        self.folded = folded if folded is not None else 0


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

# Phase 1: Restructure Your Simulator
# Split your Table.start() into:
# reset() → initializes deck, deals hole cards, sets phase = preflop.
# step(action) → advances the game one decision/action at a time.
# Stop auto-running all the phases; let actions drive transitions.

    def start(self):
        # resets()
        reset_everything()

        self.preflop()
        self.flop()
        self.turn()
        self.river()
        self.showdown()

    def preflop(self):
        print(self.phase)       
        # shuffle the deck
        random.shuffle(self.deck)

        # small blinds and big blinds
        number_players = len(players)
        dealer_index = 0
        small_blind_index = (dealer_index + 1) % number_players
        big_blind_index = (dealer_index + 2) % number_players
        SMALL_BLIND = 10
        BIG_BLIND = SMALL_BLIND * 2
        # subtract money from players
        self.players[small_blind_index].money -= SMALL_BLIND
        self.players[big_blind_index].money -= BIG_BLIND
        # add to the pot
        self.pot += SMALL_BLIND + BIG_BLIND

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

        # decision of players != initial blinds
        player3_index = big_blind_index = (dealer_index + 3) % number_players
        for i in range(player3_index, len(number_players)):
            # has 3 decisions: Fold, Call 2 (match the big blind), or Raise (must be at least 4 total here).
            decision_preflop = input('Fold(1), Call(2), Raise(3)')
            if decision_preflop == 1:
                self.players[i].folded = 1
            elif decision_preflop == 2:
                self.players[i].money -= BIG_BLIND
                self.pot += BIG_BLIND
            elif decision_preflop == 3:
                raise_preflop = input(f'How much would you like to raise (min{BIG_BLIND*2})')
                self.players[i].money -= raise_preflop
                self.pot += raise_preflop
                BIG_BLIND = raise_preflop
        
        # decisions of small player blind
# If nobody raised yet: they already posted 1, so to Call they only need to add 1 more (to match the Big Blind of 2). 
# They can also Raise or Fold.
# If there was a raise: they need to put in enough chips to match that new higher bet.
        decision_small_blind_player = input(f'Fold(1), Call(2) min needed:{BIG_BLIND-SMALL_BLIND}, Raise(3)')
        if decision_small_blind_player == 1:
            self.players[small_blind_index].folded = 1
        elif decision_small_blind_player == 2:
            self.players[small_blind_index].money -= BIG_BLIND
            self.pot += BIG_BLIND
        elif decision_small_blind_player == 3:
            raise_preflop = input(f'How much would you like to raise (min{BIG_BLIND*2})')
            self.players[small_blind_player].money -= raise_preflop
            self.pot += raise_preflop
            BIG_BLIND = raise_preflop
        
        # decisions of big player blind
# If nobody raised: the BB already put in 2, so they can Check (do nothing and see the flop).
# If there was a raise: they must either Fold, Call the raise, or Re-raise.
        decision_big_blind_player = input(f'Fold(1), Call(2) min needed:{BIG_BLIND-SMALL_BLIND}, Raise(3), Check(4)')
        if decision_big_blind_player == 1:
            self.players[big_blind_index].folded = 1
        elif decision_big_blind_player == 2:
            self.players[big_blind_index].money -= BIG_BLIND
            self.pot += BIG_BLIND
        elif decision_big_blind_player == 3:
            raise_preflop = input(f'How much would you like to raise (min{BIG_BLIND*2})')
            self.players[big_blind_index].money -= raise_preflop
            self.pot += raise_preflop
            BIG_BLIND = raise_preflop
        elif decision_big_blind_player == 4:
            print('Check')

        
        dealer_index = (dealer_index + 1) % number_players
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
            
            # cleaning hands
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
            
            
            # evaluate hands
            player.strongest_hand = evaluate_hand(player.shared_hand)
            
            print(f'Player {player.name} has {player.strongest_hand}')
            decoded = decode_hand(player.strongest_hand)
            print(f'Player {player.name} has {decoded}')


        # show community cards
        print(f'community cards: {self.show_up_cards()}')


        # TODO MONEY TRANSFERS

        # reset everything

        reset_everything()

if __name__ == "__main__":
    p1 = Player('A', 100)
    p2 = Player('B', 100)
    p3 = Player('C', 100)

    players = [p1, p2, p3]
    game_table = Table(players)
    game_table.start()