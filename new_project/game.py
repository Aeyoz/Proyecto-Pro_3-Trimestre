from __future__ import annotations
from cards import Card, Hand
import roles


def get_winner(
    players: list[roles.Player],
    common_cards: list[Card],
    private_cards: list[list[Card]],
) -> tuple[roles.Player | None, Hand]:
    p1, p2 = players
    p1.cards, p2.cards = private_cards
    p1.common_cards = p2.common_cards = common_cards
    p1.get_best_combination()
    p2.get_best_combination()
    if p1.punctuation > p2.punctuation:
        return p1.name
    elif p1.punctuation < p2.punctuation:
        return p2.name
    return None


# print(
#    get_winner(
#        [Player("Player 1"), Player("Player 2")],
#        [Card("J◆"), Card("3♣"), Card("K♣"), Card("K◆"), Card("5◆")],
#        [[Card("J♣"), Card("8◆")], [Card("9❤"), Card("10♠")]],
#    )
# )
# for card1, card2 in zip(p1, p2):
#    if card1 == card2:
#        tie = True
#    if card1 > card2:
#        "algo"
#    if card2 > card1:
#        "algo"

# new_game = Game(7)
# print(new_game.start_game())
#        "8,3,1,2,8 CAT = 2 RANK = 8"
#        "8 2 3 8 2 CAT = 3 RANK = (8, 2)"
#        "8 8 2 1 3 -> 1 2 3 CAT = 2 RANK = 8"
#        "8 8 5 6 10 -> 5 6 10 CAT = 2 RANK = 8"
#        "3,3,3,5,9 -> CAT = 4 RANK = 3 (5 9)"
#
#        for card1, card2 in zip(p1.hand.hand_values, p2.hand.hand_values):
#            if card1 > card2:
#                return p1.name, p1.hand.hand_values
#            if card1 < card2:
#                return p2.name, p2.hand.hand_values
