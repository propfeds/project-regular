class Rect:
    def __init__(self, x, y, w, h):
        self.x1=x
        self.y1=y
        self.x2=x+w
        self.y2=y+h
    
    def centre(self):
        cen_x=int((self.x1+self.x2)/2)
        cen_y=int((self.y1+self.y2)/2)
        return (cen_x, cen_y)

    def intersect(self, ref):
        # True if the two rects intersect (condition's slightly different than tutorial, BUT MAKE SENSE, to fit more rooms, more monsters and more grinding, this is the Circle of Angband anyway)
        return (self.x1<=ref.x2 and self.x2>ref.x1 and self.y1<=ref.y2 and self.y2>ref.y1)