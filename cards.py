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

    def __lt__(self, other: Card):
        return self.cmp_value < other.cmp_value

    def __gt__(self, other: Card):
        return self.cmp_value > other.cmp_value

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

    @property
    def random_card(self) -> Card:
        return self.cards[helpers.randint(1, len(self))]

    @property
    def top_card(self) -> Card:
        return self.cards[0]

    @property
    def bottom_card(self) -> Card:
        return self.cards[-1]

    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, index):
        return self.cards[index]
    
new_deck = Deck()

print(new_deck.bottom_card)
