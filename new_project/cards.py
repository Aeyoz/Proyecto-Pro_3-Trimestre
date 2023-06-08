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
        self.hand_values = []
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
        for i in self.combination:
            if i.value == 1:
                if sum(i.value for i in self.combination) == 15:
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
    def cat_rank(self) -> str | tuple:
        if len(self.pattern_values) == len(self.values):
            highest_card = max(self.pattern_values.keys())
            return Card.SYMBOLS[highest_card - 1] if highest_card != 14 else "A"
        pattern = list(self.pattern_values.values())
        better_card_values = []
        other_values = []
        for key, value in self.pattern_values.items():
            if value in pattern and value != 1:
                better_card_values.append(
                    Card.SYMBOLS[key - 1] if key != 14 else "A"
                )
            else:
                other_values.append(key)
        other_values = []
        self.hand_values = []
        for key, value in self.pattern_values.items():
            if value != 1:
                self.hand_values.extend([key] * value)
            else:
                other_values.append(key)
        self.hand_values = list(sorted(self.hand_values,reverse=True))
        self.hand_values.extend(other_values)
        return (
            "".join(better_card_values)
            if len(better_card_values) == 1
            else tuple(sorted(better_card_values, reverse=True))
            if self.cat == 3
            else tuple(sorted(better_card_values))
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

    def __str__(self) -> str:
        return f"{self.hand_values}"

    def __contains__(self, other: Card) -> bool:
        return other in self.combination

    def __gt__(self, other: Hand) -> bool:
        if self.cat > other.cat:
            return True
        if other.cat > self.cat:
            return False
        if self.cat == Hand.TWO_PAIR or self.cat == Hand.FULL_HOUSE:
            for item1, item2 in zip(self.cat_rank, other.cat_rank):
                card1 = Card.SYMBOLS.index(item1) + 1
                card2 = Card.SYMBOLS.index(item2) + 1
                if card1 > card2:
                    print(f"Gana{card1}, {card2}")
                    return True
                if card2 > card1:
                    print(f"Pierde{card1}, {card2}")
                    return False
        for card_num1, card_num2 in zip(self.hand_values, other.hand_values):
            if card_num1 > card_num2:
                return True
            if card_num1 < card_num2:
                return False
        return False


#new_hand = Hand((Card('A❤'), Card('9❤'), Card('K❤'), Card('K♠'), Card('A◆')))
#print(new_hand.cat_rank)
#
#new_hand2 = Hand((Card('2♠'), Card('8❤'), Card('4♠'), Card('4◆'), Card('2◆')))
#print(new_hand2.cat_rank)
#print(new_hand2.hand_values)