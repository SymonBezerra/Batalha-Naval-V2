SHIP_TAGS = {"R": "Carrier", "B": "Battleship",
            "C": "Cruiser", "D": "Destroyer"}
SHIP_SIZES = {"R": 5, "B": 4, "C": 3, "D": 2}
class Ship:
    def __init__(self, type: str):
        self.name = SHIP_TAGS[type]
        self.size = SHIP_SIZES[type]