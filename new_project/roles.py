from __future__ import annotations
import helpers
from cards import Hand


class Player:
    def __init__(self, name: str):
        self.name = name

    def get_best_combination(self) -> Hand:
        player_cards = self.cards + self.common_cards
        hand = ()
        for iter in helpers.combinations(player_cards, n=5):
            hand_comb = Hand(iter)
            if not hand or hand_comb > hand:
                hand = hand_comb
        return hand
