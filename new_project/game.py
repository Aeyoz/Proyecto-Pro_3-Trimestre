from __future__ import annotations
from cards import Card, Hand
from roles import Player


def get_winner(
    players: list[Player], common_cards: list[Card], private_cards: list[list[Card]]
) -> tuple[Player | None, Hand]:
    p1, p2 = players
    p1.cards, p2.cards = private_cards
    # print(p1.name, p1.cards)
    # print(p2.name, p2.cards)
    p1.common_cards = p2.common_cards = common_cards
    p1.hand = p1.get_best_combination()
    # print(p1.hand)
    p2.hand = p2.get_best_combination()
    # print(p2.hand)
    print(p1.hand.hand_values)
    print(p2.hand.hand_values)
    if p1.hand > p2.hand:
        return p1, p1.hand
    if p2.hand > p1.hand:
        return p2, p2.hand
    return None, p1.hand


print(
    get_winner(
        [Player("Player 1"), Player("Player 2")],
        [Card("K❤"), Card("2♠"), Card("K♠"), Card("2◆"), Card("A◆")],
        [[Card("A❤"), Card("9❤")], [Card("6❤"), Card("5♣")]],
    )
)


    pytest.param(
        [Player('Player 1'), Player('Player 2')],
        [Card('A❤'), Card('9♠'), Card('3◆'), Card('3❤'), Card('2◆')],
        [[Card('7♠'), Card('4◆')], [Card('5♠'), Card('4❤')]],
        'Player 1',
        [Card('3◆'), Card('3❤'), Card('A❤'), Card('9♠'), Card('7♠')],
        Hand.ONE_PAIR,
        '3',
        id="9",
    ),