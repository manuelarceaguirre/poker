from draft import evaluate_hand

def test_high_card():
    # Just junk, no pairs, no flush, no straight
    hand = [(2,0), (5,1), (7,2), (9,3), (11,0), (3,1), (6,2)]
    assert evaluate_hand(hand) == 0  # High Card

def test_one_pair():
    hand = [(2,0), (2,1), (5,2), (7,3), (9,0), (11,1), (3,2)]
    assert evaluate_hand(hand) == 1  # One Pair

def test_two_pair():
    hand = [(2,0), (2,1), (5,0), (5,1), (9,2), (11,3), (7,0)]
    assert evaluate_hand(hand) == 2  # Two Pair

def test_three_of_a_kind():
    hand = [(7,0), (7,1), (7,2), (5,0), (9,1), (11,2), (3,3)]
    assert evaluate_hand(hand) == 3  # Trips

def test_straight_low_ace():
    # A-2-3-4-5 straight
    hand = [(0,0), (1,1), (2,2), (3,0), (4,3), (9,1), (11,2)]
    assert evaluate_hand(hand) == 4  # Straight

def test_straight_high_ace():
    # 10-J-Q-K-A straight
    hand = [(0,0), (9,1), (10,2), (11,3), (12,0), (4,1), (6,2)]
    assert evaluate_hand(hand) == 4  # Straight

def test_flush():
    # 5 cards of suit 0
    hand = [(2,0), (5,0), (7,0), (9,0), (11,0), (3,1), (6,2)]
    assert evaluate_hand(hand) == 5  # Flush

def test_full_house():
    # 3 sevens + 2 fives
    hand = [(7,0), (7,1), (7,2), (5,0), (5,1), (9,2), (11,3)]
    assert evaluate_hand(hand) == 6  # Full House

def test_four_of_a_kind():
    hand = [(2,0), (2,1), (2,2), (2,3), (9,0), (11,1), (3,2)]
    assert evaluate_hand(hand) == 7  # Quads

def test_straight_flush():
    # 5-6-7-8-9 of suit 0
    hand = [(5,0), (6,0), (7,0), (8,0), (9,0), (2,1), (11,2)]
    assert evaluate_hand(hand) == 8  # Straight Flush
