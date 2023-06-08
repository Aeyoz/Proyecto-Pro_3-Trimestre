from __future__ import annotations
import helpers
import cards


class Player:
    def __init__(self, name: str):
        self.name = name

    def get_best_combination(self):
        #player_cards = list(card for card in self.cards)
        #common_cards = list(card for card in self.common_cards)
        #player_cards.extend(common_cards)
        player_cards = self.cards + self.common_cards 
        hand = ()
        for iter in helpers.combinations(player_cards, n=5):
            #print([f"{card.value}{card.suit}" for card in iter])
            hand_comb = cards.Hand(iter)
            if not hand or hand_comb > hand:
                hand = hand_comb
        return hand

p1 = Player("Player 1")    
p2 = Player("Player 2")    
p1.common_cards = p2.common_cards = [cards.Card('5❤'), cards.Card('9♠'), cards.Card('4◆'), cards.Card('2◆'), cards.Card('7◆')]
p1.cards = [cards.Card('K◆'), cards.Card('3❤')]
p2.cards = [cards.Card('Q♣'), cards.Card('J❤')]
p1.hand = p1.get_best_combination()
p2.hand = p2.get_best_combination()
print(p1.hand)
print(p2.hand)
print(p1.hand > p2.hand)
