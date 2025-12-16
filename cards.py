import random

def new_deck():
    ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    suits = ['♠','♥','♦','♣']
    deck = [{'rank': r, 'suit': s} for r in ranks for s in suits]
    random.shuffle(deck)
    return deck

def card_value(card):
    if card['rank'] in ['J','Q','K']:
        return 10
    if card['rank'] == 'A':
        return 11
    return int(card['rank'])

def calc_best_total(hand):
    total = sum(card_value(c) for c in hand)
    aces = sum(1 for c in hand if c['rank'] == 'A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total
