from __future__ import annotations
import helpers
from cards import Card, Hand


class Player:
    def __init__(self, name: str):
        self.name = name

    def get_best_combination(self):
        player_cards = self.cards + self.common_cards 
        hand = ()
        for iter in helpers.combinations(player_cards, n=5):
            #print([f"{card.value}{card.suit}" for card in iter])
            hand_comb = Hand(iter)
            if not hand or hand_comb > hand:
                hand = hand_comb
        return hand
    
p1 = Player('Player 1')
p2 = Player('Player 2')
p1.common_cards = p2.common_cards = [Card('A◆'), Card('J❤'), Card('9◆'), Card('8❤'), Card('8♣')]
p1.cards, p2.cards = [Card('10♣'), Card('10❤')], [Card('5♣'), Card('2❤')]
p1.hand = p1.get_best_combination()
p2.hand = p2.get_best_combination()
print(p1.hand)
print(p1.hand.cat_rank)