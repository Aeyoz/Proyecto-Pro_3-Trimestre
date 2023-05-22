from __future__ import annotations
import cards
import roles


class Game:
    def __init__(self, number_of_players: int):
        self.deck = cards.Deck()
        self.players = [
            roles.Player(f"Player{i}") for i in range(1, number_of_players + 1)
        ]
        self.dealer = roles.Dealer()
        self.dealer.players = self.players

    def start_game(self):
        for player in self.players:
            player.cards = [self.dealer.give_players_cards()]
        common_cards = self.dealer.show_comunity_cards()


new_game = Game(7)
print(new_game.players[0].name)