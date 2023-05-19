from __future__ import annotations
import cards
import roles


class Game:
    def __init__(self):
        self.deck = cards.Deck()
        player1 = roles.Player("Player1")
        player2 = roles.Player("Player2")
        self.players = [player1, player2]
        self.dealer = roles.Dealer()
