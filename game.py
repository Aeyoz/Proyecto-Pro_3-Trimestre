from __future__ import annotations
import cards
import roles


class Game:
    def __init__(self, number_of_players: int):
        self.players = [
            roles.Player(f"Player{i}") for i in range(1, number_of_players + 1)
        ]

    def start_game(self):
        self.dealer = roles.Dealer()
        self.deck = self.dealer.deck = cards.Deck()
        self.dealer.deck.shuffle_deck()
        self.dealer.players = self.players
        self.community_cards = self.dealer.display_community_cards()
        #self.community_cards = [cards.Card(3, "♣"), cards.Card(3, "◆"), cards.Card(6, "♠"), cards.Card(12, "♠"), cards.Card(6, "❤")]
        print(" |  ".join(f"{card.value}{card.suit}" for card in self.community_cards))
        for player in self.players:
            #player.cards = [cards.Card(1, "◆"), cards.Card(9, "◆")]
            player.get_cards(self.dealer)
            print(player.name)
            print(" |  ".join(f"{card.value}{card.suit}" for card in player.cards))
            player.common_cards = self.community_cards
            player.best_combination = player.get_best_combination() + (player.name,)
            print(player.best_combination)
            print("\n")
        game_combs = list(player.best_combination for player in self.players)
        return game_combs

new_game = Game(4)
new_game.start_game()
