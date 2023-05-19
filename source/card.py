from __future__ import annotations
import helpers


class Card:
    CLUBS = "♣"
    DIAMONDS = "◆"
    HEARTS = "❤"
    SPADES = "♠"
    GLYPH = {
        "♣": "🃑🃒🃓🃔🃕🃖🃗🃘🃙🃚🃛🃝🃞",
        "◆": "🃁🃂🃃🃄🃅🃆🃇🃈🃉🃊🃋🃍🃎",
        "❤": "🂱🂲🂳🂴🂵🂶🂷🂸🂹🂺🂻🂽🂾",
        "♠": "🂡🂢🂣🂤🂥🂦🂧🂨🂩🂪🂫🂭🂮",
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

    def __lt__(self, other: Card):
        return self.cmp_value < other.cmp_value

    def __gt__(self, other: Card):
        return self.cmp_value > other.cmp_value

    def __str__(self):
        return Card.GLYPHS[self.suit][self.value - 1]


class Deck:
    def __init__(self):
        self.cards = []
        for suit in Card.GLYPH.keys():
            for num in range(1, 13 + 1):
                self.cards.append(Card(num, suit))

    @property
    def get_random_card(self):

