from __future__ import annotations
import helpers


class Card:
    CLUBS = "♣"
    DIAMONDS = "◆"
    HEARTS = "❤"
    SPADES = "♠"
    GLYPH = {
        CLUBS: "🃑🃒🃓🃔🃕🃖🃗🃘🃙🃚🃛🃝🃞",
        DIAMONDS: "🃁🃂🃃🃄🃅🃆🃇🃈🃉🃊🃋🃍🃎",
        HEARTS: "🂱🂲🂳🂴🂵🂶🂷🂸🂹🂺🂻🂽🂾",
        SPADES: "🂡🂢🂣🂤🂥🂦🂧🂨🂩🂪🂫🂭🂮",
    }
    A_VALUE = 1
    K_VALUE = 13
    A_OTHER_VALUE = 14

    def __init__(self, value: int, suit: str):
        self.value = value
        self.suit = suit

    @property
    def cmp_value(self):
        if self.value == 1:
            return 14
        return self.value

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.value == other.value and self.suit == other.suit
        return False

    def __gt__(self, other: Card):
        return self.cmp_value > other.cmp_value

    def __lt__(self, other: Card):
        return self.cmp_value < other.cmp_value

    def __str__(self):
        return Card.GLYPH[self.suit][self.value - 1]


class Deck:
    def __init__(self):
        self.cards = []
        for suit in Card.GLYPH.keys():
            for num in range(1, 13 + 1):
                self.cards.append(Card(num, suit))

    def get_random_card(self) -> Card:
        deck_length = len(self) - 1
        return self.cards.pop(helpers.randint(1, deck_length))

    def reset_deck(self):
        self.cards = Deck().cards

    def shuffle_deck(self):
        helpers.shuffle(self.cards)

    def get_top_card(self):
        return self.cards.pop(0)

    def get_bottom_card(self):
        return self.cards.pop()

    @property
    def top_card(self) -> Card:
        return self.cards[0]

    @property
    def bottom_card(self) -> Card:
        return self.cards[-1]

    def __len__(self):
        return len(self.cards)


class Hand:
    def __init__(self, *best_combination: tuple):
        self.best_combination = best_combination
        self.ranking = {
            "escalera_real": 500,  # Escalera real
            "escalera_de_color": 250,  # Escalera de color
            (4, 1): 100,  # Poker
            (3, 2): 90,  # Full
            "color": 80,  # Color
            (1, 1, 1, 1, 1, True): 70,  # Escalera sin color
            (3, 1, 1): 60,  # Trio
            (2, 2, 1): 50,  # Doble pareja
            (2, 1, 1, 1): 40,  # Pareja
            (1, 1, 1, 1, 1, False): 30,  # Carta alta
        }

    # mismo palo
    #    10,11,12,13,14 = "escalera real" = 60
    #    "escalera_de_color" = sum(comb) != 60
    #    "color" = sum(comb) != 60 and not conscutive

    # no mismo palo
    #    4 * card.value (4,4,4,4, 11) {4:4, 11:1} (4,1) : 20
    #    3 * card.value + 2 * card.value (2,2,2,3,3) {2:3, 3:2} (3,2)
    #    1 + 2 + 3 + 4 + 5 (1,1,1,1,1, True)
    #    3 * card.value (2,2,2,3,4) {2:3, 3:1, 4:1} (3,1,1)
    #    2 * card.value + 2 * card.value (2,2,4,5,4) {2:2,4:2,5:1} (2,2,1)
    #    2 * card.value (2,2,4,5,6) {2:2, 4:1, 5:1, 6:1} (2,1,1,1)
    #    get_best_card (1,1,1,1,1, False)

    # best_combination = (obj, obj, obj, obj, obj)

    @property
    def values(self):
        to_compare_values = []
        for i in self.best_combination:
            if i.value == 1:
                if sum(i.cmp_value for i in self.best_combination) != 60:
                    to_compare_values.append(1)
                else:
                    to_compare_values.append(14)
                continue
            to_compare_values.append(i.cmp_value)
        return sorted(to_compare_values)

    def get_ranking(self):
        if isinstance(self.is_royal(), str):
            return self.ranking[self.is_royal()]
        if self.same_suits():
            return self.ranking["color"]
        if self.consecutive():
            """"""
        numbers = set(self.values)

        pass

    def same_suits(self):
        return self.best_combination[0].suit * 5 == "".join(
            i.suit for i in self.best_combination
        )

    def is_royal(self):
        if self.same_suits() and sum(self.values) == 60:
            return "escalera_real"
        if self.same_suits() and self.consecutive():
            return "escalera_de_color"
        return False

    def consecutive(self):
        fcard = self.values[0]
        for card in self.values[1:]:
            if (card - 1) != fcard:
                return False
            fcard = card
        return True


#    suit_element_0 = elements[0].suit
#    for i in elements[1:]:
#        if i.suit != suit_element_0:
#            return False
#        return True


a = Deck()

card1 = Card(1, Card.HEARTS)
card2 = Card(2, Card.HEARTS)
card3 = Card(3, Card.HEARTS)
card4 = Card(4, Card.HEARTS)
card5 = Card(5, Card.HEARTS)

mano = Hand(card2, card3, card1, card4, card5)

print(mano.best_combination[0])
print(mano.same_suits())
print(mano.consecutive())
