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
        if self.value == Card.A_VALUE:
            return Card.A_OTHER_VALUE
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
    deck = []
    for suit in Card.GLYPH.keys():
        for num in range(1, 13 + 1):
            deck.append(Card(num, suit))

    def __init__(self):
        pass

    def get_random_card(self) -> Card:
        deck_length = len(self) - 1
        return self.deck.pop(helpers.randint(1, deck_length))

    def reset_deck(self):
        self.deck = Deck().generate_cards()

    def shuffle_deck(self):
        helpers.shuffle(self.deck)

    def get_top_card(self):
        return self.deck.pop(0)

    def get_bottom_card(self):
        return self.deck.pop()

    @property
    def top_card(self) -> Card:
        return self.deck[0]

    @property
    def bottom_card(self) -> Card:
        return self.deck[-1]

    def __len__(self):
        return len(self.deck)

    def __str__(self):
        return f"{hex(id(self))}"


class Hand:
    def __init__(self, combination: tuple):
        self.combination = combination
        self.ranking = {
            "escalera_real": 500,  # Escalera real
            "escalera_de_color": 250,  # Escalera de color
            (4, 1): 100,  # Poker
            (3, 2): 90,  # Full
            "color": 80,  # Color
            "stair": 70,  # Escalera sin color
            (3, 1, 1): 60,  # Trio
            (2, 2, 1): 50,  # Doble pareja
            (2, 1, 1, 1): 40,  # Pareja
            (1, 1, 1, 1, 1): 30,  # Carta alta
        }

    # mismo palo
    #    10,11,12,13,14 = "escalera real" = 60
    #    "escalera_de_color" = sum(comb) != 60
    #    "color" = sum(comb) != 60 and not conscutive

    # no mismo palo
    #    4 * card.value (4,4,4,4, 11) {4:4, 11:1} (4,1)
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
        for i in self.combination:
            if i.value == 1:
                if sum(i.value for i in self.combination) == 15:
                    to_compare_values.append(1)
                else:
                    to_compare_values.append(14)
                continue
            to_compare_values.append(i.cmp_value)
        return sorted(to_compare_values)

    def get_ranking(self):
        is_stair, hand_value = self.is_stair
        highest_card = max(self.values)
        if is_stair:
            return self.ranking[hand_value]["punctuation"], highest_card
        if self.same_suits() and not self.consecutive:
            return self.ranking["color"]["punctuation"], highest_card
        ranking, value = self.get_patern()
        return self.ranking[ranking]["punctuation"], value

    def get_patern(self):
        pattern_values = {item: self.values.count(item) for item in set(self.values)}
        return tuple(sorted(pattern_values.values(), reverse=True)), max(
            pattern_values.keys()
        )

    def same_suits(self):
        return self.combination[0].suit * 5 == "".join(i.suit for i in self.combination)

    @property
    def is_stair(self):
        if self.same_suits() and sum(self.values) == 60:
            return True, "escalera_real"
        if self.same_suits() and self.consecutive:
            return True, "escalera_de_color"
        if self.consecutive:
            return True, "stair"
        return False, None

    @property
    def consecutive(self):
        fcard = self.values[0]
        for card in self.values[1:]:
            if (card - 1) != fcard:
                return False
            fcard = card
        return True


"""
a = Deck()
"""

card1 = Card(1, Card.HEARTS)
card2 = Card(2, Card.HEARTS)
card3 = Card(6, Card.HEARTS)
card4 = Card(4, Card.SPADES)
card5 = Card(5, Card.CLUBS)
card6 = Card(10, Card.SPADES)
card7 = Card(11, Card.SPADES)
card8 = Card(12, Card.SPADES)
card9 = Card(13, Card.SPADES)
card10 = Card(1, Card.SPADES)
card11 = Card(2, Card.CLUBS)
card12 = Card(5, Card.CLUBS)
card13 = Card(3, Card.CLUBS)
card14 = Card(7, Card.CLUBS)
card15 = Card(8, Card.CLUBS)
card16 = Card(9, Card.HEARTS)
card17 = Card(4, Card.SPADES)
card18 = Card(3, Card.CLUBS)
card19 = Card(2, Card.DIAMONDS)
card20 = Card(7, Card.HEARTS)

mano = Hand((card2, card3, card1, card4, card5))  # 250
mano1 = Hand((card6, card7, card8, card9, card10))  # 500
mano2 = Hand((card11, card12, card13, card14, card15))  # 80
mano4 = Hand((card16, card17, card18, card19, card20))  # 30
"""
print(mano.combination[0])
print(mano.same_suits())
print(mano.get_patern())
print(mano.get_ranking())
print(mano1.get_ranking())
print(mano2.get_ranking())
print(mano4.get_ranking())"""
