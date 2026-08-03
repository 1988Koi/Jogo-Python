from dataclasses import dataclass
from enum import IntEnum
import random

class Suit(IntEnum):
    MAN = 0
    PIN = 1
    SOU = 2
    HONOR = 3

@dataclass(frozen=True, order=True)
class Tile:
    suit: Suit
    value: int

    def __repr__(self):
        if self.suit == Suit.HONOR:
            names = ["", "East", "South", "West", "North", "White", "Green", "Red"]
            return names[self.value]
        suit_letters = {Suit.MAN: "m", Suit.PIN: "p", Suit.SOU: "s"}
        return f"{self.value}{suit_letters[self.suit]}"

    def build_wall():
        tiles = []

        for suit in [Suit.MAN, Suit.PIM, Suit.SOU]:
            for value in range(1, 10):
                for _ in range(4):
                    tiles.append(Tile(suit, value))
        for value in range (1, 8):
            for _ in range (4):
                tiles.append(Tile(Suit.HONOR, value))

        random.shuffle(tiles)
        return tiles

    def deal_hands(wall):
        hands = []
        for _ in range(4):
            hand = wall[:13]
            wall = wall[13:]
            hands.append(hand)
        return hands, wall