import gtk


class Fractal:
    offImage = None
    colorMap = None
    color = None
    gc = None

    def __init__(self):
        print "Fractal.__init__"
        self.offImage = gtk.gdk.Pixmap(None, 600, 600, 24)
        self.colorMap = gtk.gdk.colormap_get_system()
        self.color = self.colorMap.alloc_color("white")
        self.gc = self.offImage.new_gc(self.color)
        self.offImage.draw_rectangle(self.gc, True, 0, 0, 600, 600)
        self.color = self.colorMap.alloc_color("black")
        self.gc = self.offImage.new_gc(self.color)
        return
    
    def getName(self):
        return ""
    
    def drawing(self):
        return
    
    def getDrawable(self):
        return self.offImage
    
    def getControlPanel(self):
        return None
    
    def drawLine(self, x1, y1, x2, y2):
        realX1 = x1 + 300
        realX2 = x2 + 300
        realY1 = 300 - y1
        realY2 = 300 - y2
        self.offImage.draw_line(self.gc, int(realX1), int(realY1), int(realX2), int(realY2))
        return
    
    def stopDrawing(self):
        return
    
    def cleanAll(self):
        color = self.colorMap.alloc_color("white")
        gc = self.offImage.new_gc(color)
        self.offImage.draw_rectangle(gc, True, 0, 0, 600, 600)
        return
    