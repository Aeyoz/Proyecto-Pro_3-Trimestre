from __future__ import annotations
import helpers
import cards


class Player:
    def __init__(self, name: str):
        self.name = name

    def get_best_combination(self):
        pass

    # A la hora de comprobar las combinaciones hay que ver si el A está en juego
    # en ese caso, se pasarán 8 números para comprobar las combinaciones

    def get_cards(self, other: Dealer):
        self.cards = other.give_players_cards()


class Dealer:
    def __init__(self):
        self.name = "a"

    def give_players_cards(
        self,
    ):
        return [cards.a.get_random_card()] * 2

    def show_comunity_cards(self):
        return [cards.a.get_random_card()] * 5


a = Dealer()

print(a.give_players_cards())
