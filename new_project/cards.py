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

    def __init__(self, card_representation: str):
        *str_value, suit = card_representation
        self.suit = suit
        self.str_value = "".join(str_value)
        self.value = Card.SYMBOLS.index(self.str_value) + 1

    @classmethod
    def get_symbol(cls, card_num):
        return Card.SYMBOLS[card_num - 1] if card_num != 14 else "A"

    @classmethod
    def get_value(cls, card_symbol, is_cmp=True):
        if is_cmp:
            return (
                Card.SYMBOLS.index(card_symbol) + 1
                if card_symbol not in ("A","1","0")
                else Card.A_VALUE + Card.K_VALUE
            )
        return Card.SYMBOLS.index(card_symbol) + 1

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

    def __repr__(self) -> str:
        return f"{self.str_value}{self.suit}"


class Hand:
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    def __init__(self, combination: tuple):
        self.combination = combination
        self.pattern_values = {
            item: self.values.count(item) for item in set(self.values)
        }
        self.is_cmp = max(self.total_sum) > 5
        self.ranking = {
            "escalera_real": Hand.ROYAL_FLUSH,  # Escalera real
            "escalera_de_color": Hand.STRAIGHT_FLUSH,  # Escalera de color
            (4, 1): Hand.FOUR_OF_A_KIND,  # Poker
            (3, 2): Hand.FULL_HOUSE,  # Full
            "color": Hand.FLUSH,  # Color
            "stair": Hand.STRAIGHT,  # Escalera sin color
            (3, 1, 1): Hand.THREE_OF_A_KIND,  # Trio
            (2, 2, 1): Hand.TWO_PAIR,  # Doble pareja
            (2, 1, 1, 1): Hand.ONE_PAIR,  # Pareja
            (1, 1, 1, 1, 1): Hand.HIGH_CARD,  # Carta alta
        }

    @property
    def values(self) -> list:
        to_compare_values = []
        self.total_sum = list(i.value for i in self.combination)
        for i in self.combination:
            if i.value == 1:
                if max(self.total_sum) < 5:
                    to_compare_values.append(1)
                else:
                    to_compare_values.append(i.cmp_value)
                continue
            to_compare_values.append(i.cmp_value)
        return sorted(to_compare_values)
    
    @property
    def cat(self) -> int:
        is_stair, hand_value = self.is_stair
        if is_stair:
            return self.ranking[hand_value]
        if self.same_suits() and not self.consecutive:
            return self.ranking["color"]
        ranking = tuple(sorted(self.pattern_values.values(), reverse=True))
        return self.ranking[ranking]

    @property
    def hand_values(self):
        other_values = []
        hand_values = []
        for key, value in self.pattern_values.items():
            if value != 1:
                hand_values.extend([key] * value)
            else:
                other_values.append(key)
        hand_values = list(sorted(hand_values, reverse=True))
        other_values.sort()
        hand_values.extend(other_values)
        return hand_values

    @property
    def cat_rank(self) -> str | tuple:
        if len(self.pattern_values) == len(self.values):
            highest_card = max(self.pattern_values.keys())
            return Card.SYMBOLS[highest_card - 1] if highest_card != 14 else "A"
        pattern = list(self.pattern_values.values())
        better_card_values = []
        other_values = []
        for key, value in self.pattern_values.items():
            if value in pattern and value != 1:
                better_card_values.append(Card.SYMBOLS[key - 1] if key != 14 else "A")
            else:
                other_values.append(key)
        if len(better_card_values) == 1:
            return "".join(better_card_values)
        if self.cat == Hand.TWO_PAIR:
            item1, item2 = better_card_values
            if Card.get_value(item1) > Card.get_value(item2):
                return item1, item2
            return item2, item1
#            if all(i.isalpha() for i in better_card_values):
#                return tuple(sorted(better_card_values))
#            if all(i.isnumeric() for i in better_card_values):
#                if all(len(i) == 2 for i in better_card_values):
#                    return tuple(sorted(better_card_values))
#                return tuple(sorted(better_card_values, reverse=True))
#            else:
#                return tuple(sorted(better_card_values, reverse=True))
        if self.cat == self.FULL_HOUSE:
            first_value = tuple(
                Card.SYMBOLS[item % len(Card.SYMBOLS) - 1]
                for item, value in self.pattern_values.items()
                if value == 3
            )
            second_value = tuple(
                Card.SYMBOLS[item % len(Card.SYMBOLS) - 1]
                for item, value in self.pattern_values.items()
                if value == 2
            )
            return first_value + second_value

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

    def __repr__(self) -> str:
        return f"{self.combination}"

    def __contains__(self, other: Card) -> bool:
        return other in self.combination

    def __gt__(self, other: Hand) -> bool:
        if self.cat > other.cat:
            return True
        if self.cat < other.cat:
            return False
        for card_num1, card_num2 in zip(self.hand_values, other.hand_values):
            if card_num1 > card_num2:
                return True
            if card_num1 < card_num2:
                return False
        return False