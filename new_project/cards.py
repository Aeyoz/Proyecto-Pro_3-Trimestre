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


# class Deck:
#    deck = []
#    for suit in Card.GLYPH.keys():
#        for num in range(1, 13 + 1):
#            card = str(num) + suit
#            deck.append(Card(card))
#
#    def __init__(self):
#        pass
#
#    def get_random_card(self) -> Card:
#        deck_length = len(self) - 1
#        return self.deck.pop(helpers.randint(1, deck_length))
#
#    def reset_deck(self) -> None:5
#        self.deck = Deck.deck
#
#    def shuffle_deck(self) -> None:
#        helpers.shuffle(self.deck)
#
#    def get_top_card(self) -> Card:
#        return self.deck.pop(0)
#
#    def get_bottom_card(self) -> Card:
#        return self.deck.pop()
#
#    @property
#    def top_card(self) -> Card:
#        return self.deck[0]
#
#    @property
#    def bottom_card(self) -> Card:
#        return self.deck[-1]
#
#    def __len__(self) -> int:
#        return len(self.deck)
#


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
        self.str_values = [card.str_value for card in self.combination]
        for i in self.combination:
            if i.value == 1:
                if sum(i.value for i in self.combination) == 15:
                    to_compare_values.append(1)
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
        # 3 3 3 2 2 (3, 2)
        # 2 2 4 4 1 (4, 2)
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
        complete_hand = []
        for key, value in self.pattern_values.items():
            if value in pattern and value != 1:
                better_card_values.append(
                    Card.SYMBOLS[key - 1] if key != 1 and key != 14 else "A"
                )
            else:
                other_values.append(key)
        other_values = list(sorted(other_values, reverse=True))
        self.hand_values.extend(better_card_values)
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

    def __contains__(self, other: Card) -> bool:
        return other in self.combination


# card1 = Card("A❤")
# card2 = Card("2" + Card.HEARTS)
# card3 = Card("3" + Card.HEARTS)
# card4 = Card("4" + Card.SPADES)
# card5 = Card("5" + Card.CLUBS)
# card6 = Card('10' + Card.SPADES)
# card7 = Card('11' + Card.SPADES)
# card8 = Card('12' + Card.SPADES)
# card9 = Card('13' + Card.SPADES)
# card10 = Card("A❤")
# card11 = Card(f"K{Card.CLUBS}")
# card12 = Card(f"Q{Card.CLUBS}")
# card13 = Card("K❤")
# card14 = Card("A◆")
# card15 = Card('8' + Card.CLUBS)
# card16 = Card('9' + Card.HEARTS)
# card17 = Card('4' + Card.SPADES)
# card18 = Card('3' + Card.CLUBS)
# card19 = Card('2' + Card.DIAMONDS)
# card20 = Card('7' + Card.HEARTS)
#
# mano = Hand((card10, card11, card12, card13, card14))  # 5
# mano = Hand((Card("J♣"), Card("8◆"), Card("J◆"), Card("K♣"), Card("K◆")))
# mano1 = Hand((card6, card7, card8, card9, card10))  # 500
# mano2 = Hand((card11, card12, card13, card14, card15))  # 80
# mano4 = Hand((card16, card17, card18, card19, card20))  # 30
# print(Card("J♣") in mano)
# print(mano.cat)
# print(mano.cat_rank)
