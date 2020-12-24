class Hexagon:
    def __init__(self, colour = 'w'):
        # white is default for a tile
        self._colour = colour
    
    def flip(self):
        if self._colour == 'w':
            self._colour = 'b'
        else:
            self._colour = 'w'
        
        return self

    def get_colour(self):
        return self._colour

    def __str__(self):
        return self._colour

    def __repr__(self):
        return self._colour

    @staticmethod
    def get_neighbours(coord):
        ''' Coord passed as [x, y] '''
        neighbours = []

        x = coord[0]
        y = coord[1]

        # ne
        new_x = x+1
        new_y = y+1
        neighbours.append(tuple([new_x, new_y]))

        # e
        new_x = x+2
        new_y = y
        neighbours.append(tuple([new_x, new_y]))
        
        # se
        new_x = x+1
        new_y = y-1
        neighbours.append(tuple([new_x, new_y]))

        # sw
        new_x = x-1
        new_y = y-1
        neighbours.append(tuple([new_x, new_y]))

        # w
        new_x = x - 2
        new_y = y
        neighbours.append(tuple([new_x, new_y]))

        # nw
        new_x = x-1
        new_y = y+1
        neighbours.append(tuple([new_x, new_y]))

        return neighbours
