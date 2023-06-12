from __future__ import annotations
from cards import Card, Hand
from roles import Player


def get_winner(
    players: list[Player], common_cards: list[Card], private_cards: list[list[Card]]
) -> tuple[Player | None, Hand]:
    p1, p2 = players
    p1.cards, p2.cards = private_cards
    p1.common_cards = p2.common_cards = common_cards
    p1.hand = p1.get_best_combination()
    p2.hand = p2.get_best_combination()
    if p1.hand > p2.hand:
        return p1, p1.hand
    if p2.hand > p1.hand:
        return p2, p2.hand
    return None, p1.hand
