from __future__ import annotations
import cards
import roles


class Game:
    def __init__(self, number_of_players: int):
        self.deck = cards.Deck()
        self.players = []
        for i in range(number_of_players):
            player = f"Player{i + 1}"
            self.players.append(roles.Player(player))
        self.dealer = roles.Dealer()

    def start_game(self):
        for player in self.players:
            player.cards = [self.dealer.give_players_cards()]
