from __future__ import annotations
import helpers


class Card:
    CLUBS = "♣"
    DIAMONDS = "◆"
    HEARTS = "❤"
    SPADES = "♠"
    SUITS = [CLUBS, DIAMONDS, HEARTS, SPADES]
    GLYPH = {
        CLUBS: "🃑🃒🃓🃔🃕🃖🃗🃘🃙🃚🃛🃝🃞",
        DIAMONDS: "🃁🃂🃃🃄🃅🃆🃇🃈🃉🃊🃋🃍🃎",
        HEARTS: "🂱🂲🂳🂴🂵🂶🂷🂸🂹🂺🂻🂽🂾",
        SPADES: "🂡🂢🂣🂤🂥🂦🂧🂨🂩🂪🂫🂭🂮",
    }
    SYMBOLS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
    A_VALUE = 1
    K_VALUE = 13
    FIGURES = {"A": [1, 14], "K": 13, "Q": 12, "J": 11}

    def __init__(self, card_representation: str):
        *str_value, suit = card_representation
        self.suit = suit
        self.str_value = "".join(v for v in str_value)
        self.value = Card.SYMBOLS.index(self.str_value) + 1

    @property
    def cmp_value(self):
        return Card.A_VALUE + Card.K_VALUE if self.value == Card.A_VALUE else self.value

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
            card = str(num) + suit
            deck.append(Card(card))

    def __init__(self):
        pass

    def get_random_card(self) -> Card:
        deck_length = len(self) - 1
        return self.deck.pop(helpers.randint(1, deck_length))

    def reset_deck(self) -> None:
        self.deck = Deck.deck

    def shuffle_deck(self) -> None:
        helpers.shuffle(self.deck)

    def get_top_card(self) -> Card:
        return self.deck.pop(0)

    def get_bottom_card(self) -> Card:
        return self.deck.pop()

    @property
    def top_card(self) -> Card:
        return self.deck[0]

    @property
    def bottom_card(self) -> Card:
        return self.deck[-1]

    def __len__(self) -> int:
        return len(self.deck)


class Hand:
    def __init__(self, combination: tuple):
        self.combination = combination
        self.HIGH_CARD = 1
        self.ONE_PAIR = 2
        self.TWO_PAIR = 3
        self.THREE_OF_A_KIND = 4
        self.STRAIGH = 5
        self.FLUSH = 6
        self.FULL_HOUSE = 7
        self.POKER = 8
        self.STRAIGHT_FLUSH = 9
        self.ROYAL_FLUSH = 10
        self.ranking = {
            "escalera_real": self.ROYAL_FLUSH,  # Escalera real
            "escalera_de_color": self.STRAIGHT_FLUSH,  # Escalera de color
            (4, 1): self.POKER,  # Poker
            (3, 2): self.FULL_HOUSE,  # Full
            "color": self.FLUSH,  # Color
            "stair": self.STRAIGH,  # Escalera sin color
            (3, 1, 1): self.THREE_OF_A_KIND,  # Trio
            (2, 2, 1): self.TWO_PAIR,  # Doble pareja
            (2, 1, 1, 1): self.ONE_PAIR,  # Pareja
            (1, 1, 1, 1, 1): self.HIGH_CARD,  # Carta alta
        }

    @property
    def values(self) -> list:
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

    def get_ranking(self) -> tuple:
        is_stair, hand_value = self.is_stair
        lower_card, highest_card = self.values[0], self.values[-1]
        if is_stair:
            return self.ranking[hand_value], highest_card, lower_card
        if self.same_suits() and not self.consecutive:
            return self.ranking["color"], highest_card, lower_card
        ranking, max_value, min_value = self.patern
        return self.ranking[ranking], max_value, min_value

    @property
    def patern(self) -> tuple:
        pattern_values = {item: self.values.count(item) for item in set(self.values)}
        if len(pattern_values) == len(self.values):
            return (
                tuple(sorted(pattern_values.values(), reverse=True)),
                max(pattern_values.keys()),
                min(pattern_values.keys()),
            )
        pattern = list(pattern_values.values())
        better_card_values = []
        for key, value in pattern_values.items():
            if value in pattern and value != 1:
                better_card_values.append(key)
        return (
            tuple(sorted(pattern_values.values(), reverse=True)),
            max(better_card_values),
            min(better_card_values),
        )

    def same_suits(self) -> bool:
        return self.combination[0].suit * 5 == "".join(i.suit for i in self.combination)

    @property
    def is_stair(self) -> tuple:
        if self.same_suits() and sum(self.values) == 60:
            return True, "escalera_real"
        if self.same_suits() and self.consecutive:
            return True, "escalera_de_color"
        if self.consecutive:
            return True, "stair"
        return False, None

    @property
    def consecutive(self) -> bool:
        fcard = self.values[0]
        for card in self.values[1:]:
            if (card - 1) != fcard:
                return False
            fcard = card
        return True

    def __contains__(self, other: Card) -> bool:
        return other in self.combination


# card1 = Card(1, Card.HEARTS)
# card2 = Card(2, Card.HEARTS)
# card3 = Card(3, Card.HEARTS)
# card4 = Card(4, Card.SPADES)
# card5 = Card(5, Card.CLUBS)
# card6 = Card(10, Card.SPADES)
# card7 = Card(11, Card.SPADES)
# card8 = Card(12, Card.SPADES)
# card9 = Card(13, Card.SPADES)
# card10 = Card(1, Card.SPADES)
# card11 = Card(2, Card.CLUBS)
# card12 = Card(5, Card.CLUBS)
# card13 = Card(3, Card.CLUBS)
# card14 = Card(7, Card.CLUBS)
# card15 = Card(8, Card.CLUBS)
# card16 = Card(9, Card.HEARTS)
# card17 = Card(4, Card.SPADES)
# card18 = Card(3, Card.CLUBS)
# card19 = Card(2, Card.DIAMONDS)
# card20 = Card(7, Card.HEARTS)
#
# mano = Hand((card2, card3, card1, card4, card5))  # 250
# mano1 = Hand((card6, card7, card8, card9, card10))  # 500
# mano2 = Hand((card11, card12, card13, card14, card15))  # 80
# mano4 = Hand((card16, card17, card18, card19, card20))  # 30
