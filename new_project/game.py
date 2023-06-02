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
        self.community_cards = self.dealer.display_community_cards()

    def get_winner(self):
        # print(" |  ".join(f"{card.value}{card.suit}" for card in self.community_cards))
        best_comb = ()
        for player in self.players:
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

        def get_winner(self, p1, p2):
            tie = False
            player1_punctuation, *player1_cards = p1
            player2_punctuation, *player2_cards = p2
            if (
                player1_punctuation > player2_punctuation
                or player2_punctuation > player1_punctuation
            ):
                return int(player1_punctuation > player2_punctuation)
            for card1, card2 in zip(p1, p2):
                if card1 == card2:
                    tie = True
                if card1 > card2:
                    "algo"
                if card2 > card1:
                    "algo"


new_game = Game(7)
print(new_game.start_game())
