from tiles import Tile, Suit

def can_form_sets(tiles):
    if len(tiles) == 0:
        return True

    tiles = sorted(tiles)
    first = tiles[0]

    if tiles.count(first) >= 3:
        remaining = tiles.copy()
        remaining.remove(first)
        remaining.remove(first)
        remaining.remove(first)
        if can_form_sets(remaining):
            return True

    if first.suit != Suit.HONOR:
        second = Tile(first.suit, first.value + 1)
        third = Tile(first.suit, first.value + 2)
        if second in tiles and third in tiles:
            remaining = tiles.copy()
            remaining.remove(first)
            remaining.remove(second)
            remaining.remove(third)
            if can_form_sets(remaining):
                return True

    return False

def  is_winning_hand(tiles):
    tiles = sorted(tiles)
    unique_tiles = set(tiles)

    for pair_tile in unique_tiles:
        if tiles.count(pair_tile) >= 2:
            remaining = tiles.copy()
            remaining.remove(pair_tile)
            remaining.remove(pair_tile)
            if can_form_sets(remaining):
                return True

    return False