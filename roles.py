from __future__ import annotations
import helpers
import cards


class Player:
    def __init__(self, name: str):
        self.name = name

    def get_best_combination(self):
        player_cards = list(card for card in self.cards)
        common_cards = list(card for card in self.common_cards)
        player_cards.extend(common_cards)
        hand_combs = []
        for iter in helpers.combinations(player_cards, n=5):
            # print([f"{card.value}{card.suit}" for card in iter])
            hand_combs.append(cards.Hand(iter).get_ranking())
        
        best_comb = None
        for comb in set(hand_combs):
            if best_comb == None or comb[0] > best_comb[0]:
                best_comb = comb
            if comb[0] == best_comb[0]:
                if comb[1] > best_comb[1]:
                    best_comb = comb
        return best_comb

    def get_cards(self, other: Dealer):
        self.cards = other.give_players_cards()


class Dealer:
    def __init__(self):
        self.name = "Dealer"

    def give_players_cards(self):
        return [self.deck.get_random_card() for _ in range(2)]

    def display_community_cards(self):
        return [self.deck.get_random_card() for _ in range(5)]


a = Dealer()
b = Player("Player1")

# b.get_cards(a)
# print(b.get_best_combination())
# print(a.deck)
# print(b.get_best_combination())
# print(a.give_players_cards())
# print(a.display_comunity_cards())
# print(b.cards)
# print(b.common_cards)
# print(b.get_best_combination())
# print(b.cards)
