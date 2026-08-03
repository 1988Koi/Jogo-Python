from tiles import Tile, Suit

class Hand:
    def __init__(self, tiles):
        self.tiles = list(tiles)
        self.tiles.sort()

    def draw(self, tile):
        self.tiles.append(tile)
        self.tiles.sort()

    def discard(self, tile):
        self.tiles.remove(tile)

    def __repr__(self):
        return " ".join(str(t) for t in self.tiles)