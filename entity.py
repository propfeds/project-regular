class Entity:
    def __init__(self, x, y, char, colour):
        self.x=x
        self.y=y
        self.char=char
        self.colour=colour
    def move(self, dx, dy):
        self.x+=dx
        self.y+=dy