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
        combination_cards = {f"{card.value}{card.suit}": card for card in player_cards}
        print(combination_cards.keys())
        hand = []
        for iter in helpers.combinations(player_cards, n=5):
            print([f"{card.value}{card.suit}" for card in iter])
            hand.append(cards.Hand(*iter).get_ranking())
        #            for i in iter:  # (5,1,2,3,4) i == 5, len == 5
        #                for key in combination_keys:  # (5♣,1❤,2◆,3♠,4♣,10❤,12❤), len == 7
        #                    if f"{i}" in key:  # 5 in 5♣ == True
        #                        try:
        #                            added_card = combination_cards[key]  # (5♣:5,1❤:1,2◆:2,3♠:3,4♣:4,10❤:10,12❤:12)[5♣] == 5
        #                        except KeyError:
        #                            continue
        #                        hand.append(added_card)  # hand = [obj5♣]
        #                        del combination_cards[key]  # (1❤:1,2◆:2,3♠:3,4♣:4,10❤:10,12❤:12)
        #                    continue

        return set(hand)

    # return cards.Hand(*iter).get_ranking()

    #            len(iter) == 5
    #            len(combination_cards.keys()) == 7
    #            combination_cards.keys()
    #            str(i)

    # A la hora de comprobar las combinaciones hay que ver si el A está en juego
    # en ese caso, se pasarán 8 números para comprobar las combinaciones

    def get_cards(self, other: Dealer):
        self.cards = other.give_players_cards()
        self.common_cards = other.display_comunity_cards()


class Dealer:
    def __init__(self):
        self.name = "a"
        self.deck = cards.Deck()

    def give_players_cards(self):
        return [self.deck.get_random_card() for _ in range(2)]

    def display_comunity_cards(self):
        return [self.deck.get_random_card() for _ in range(5)]


a = Dealer()
b = Player("Player1")
# print(a.deck)
b.get_cards(a)
# print(b.get_best_combination())
# print(a.give_players_cards())
# print(a.display_comunity_cards())
# print(b.cards)
# print(b.common_cards)
print(b.get_best_combination())
# print(b.cards)
