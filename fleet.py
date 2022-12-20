class Fleet:
    def __init__ (self, size: int):
        self.size = size
        self.ships = []
        # here, only the ship coordinates will be stored
        
        # for i in range(size):
        #     fleet_line = []
        #     for j in range (size):
        #         self.fleet.append((i,j))