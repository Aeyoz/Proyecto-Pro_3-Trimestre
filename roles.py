from __future__ import annotations
import helpers
import cards


class Player:
    def __init__(self, name: str):
        self.name = name

    def get_best_combination(self) -> tuple:
        player_cards = list(card for card in self.cards)
        common_cards = list(card for card in self.common_cards)
        player_cards.extend(common_cards)
        best_comb = ()
        for iter in helpers.combinations(player_cards, n=5):
            # print([f"{card.value}{card.suit}" for card in iter])
            hand_comb = cards.Hand(iter).get_ranking()
            if not best_comb or hand_comb[0] > best_comb[0]:
                best_comb = hand_comb
            if hand_comb[0] == best_comb[0]:
                if hand_comb[1] > best_comb[1]:
                    best_comb = hand_comb
                elif hand_comb[2] > best_comb[2]:
                    best_comb = hand_comb
        return best_comb

    def get_cards(self, other: Dealer) -> None:
        self.cards = other.give_players_cards()


class Dealer:
    def __init__(self):
        self.name = "Dealer"

    def give_players_cards(self) -> list:
        return [self.deck.get_random_card() for _ in range(2)]

    def display_community_cards(self) -> list:
        return [self.deck.get_random_card() for _ in range(5)]