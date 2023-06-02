from __future__ import annotations
import cards
import roles


class Game:
    def __init__(self, number_of_players: int):
        if not isinstance(number_of_players, int):
            raise ValueError(
                f"Nº players -> {number_of_players} players must be a valid integer number"
            )
        self.players = [
            roles.Player(f"Player{i}") for i in range(1, number_of_players + 1)
        ]

    def start_game(self):
        self.dealer = roles.Dealer()
        self.deck = self.dealer.deck = cards.Deck()
        self.dealer.deck.shuffle_deck()
        self.dealer.players = self.players
        self.community_cards = self.dealer.display_community_cards()
        # print(" |  ".join(f"{card.value}{card.suit}" for card in self.community_cards))
        best_comb = ()
        for player in self.players:
            player.get_cards(self.dealer)
            player.common_cards = self.community_cards
            player.best_combination = player.get_best_combination() + (player.name,)
            if not best_comb or player.best_combination[0] > best_comb[0]:
                best_comb = player.best_combination
            elif player.best_combination[0] == best_comb[0]:
                if player.best_combination[1] > best_comb[1]:
                    best_comb = player.best_combination
                elif player.best_combination[2] > best_comb[2]:
                    best_comb = player.best_combination
                elif (
                    player.best_combination[1] == best_comb[1]
                    and player.best_combination[2] == best_comb[2]
                ):
                    best_comb += (player.name, "Tie")

            punctuation, *player_cards, player_name = (80, 4, "player1")
            # print(player.name)
            # print(" |  ".join(f"{card.value}{card.suit}" for card in player.cards))
            # print(player.best_combination)
            # print("\n")
        return best_comb[-1]


new_game = Game(7)
print(new_game.start_game())

https://prod.liveshare.vsengsaas.visualstudio.com/join?1433F621983C06C1CE1CCA0B8D946990FDA0
