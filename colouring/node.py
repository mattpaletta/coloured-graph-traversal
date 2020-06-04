from colouring.colour import Colour

class Node(object):
    def __init__(self, colour: Colour, id: int):
        self._colour = colour
        self.id = id

    def get_colour(self) -> Colour:
        return self._colour
