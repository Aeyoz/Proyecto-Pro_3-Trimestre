from __future__ import annotations
import helpers
import cards


class Player:
    def __init__(self, name: str):
        self.name = name

    def get_best_combination(self):
        player_cards = list(card for card in self.cards)
        common_cards = list(card for card in self.common_cards)
        player_cards.extend(common_cards)
        hand = ()
        for iter in helpers.combinations(player_cards, n=5):
            # print([f"{card.value}{card.suit}" for card in iter])
            hand_comb = cards.Hand(iter)
            if not hand or hand_comb > hand:
                hand = hand_comb
        return hand