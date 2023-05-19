from __future__ import annotations
import helpers
import cards


class Player:
    def __init__(self, name: str):
        self.name = name

    def get_best_combination(self):
        pass


class Dealer:
    def __init__(self):
        pass

    def give_players_cards(self):
        return [cards.Deck.get_random_card()] * 2

    def show_comunity_cards(self):
        return [cards.Deck.get_random_card()] * 5


Player1 = Player("Player1")
Player2 = Player("Player2")
Player3 = Player("Player3")
