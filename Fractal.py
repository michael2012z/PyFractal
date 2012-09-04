import gtk


class Fractal:
    offImage = None
    colorMap = None
    color = None
    gc = None
    zoomHistory = []
    

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
    
    def drawPoint(self, x, y):
        realX = x + 300
        realY = 300 - y
        self.offImage.draw_point(self.gc, int(realX), int(realY))
        return
    
    def drawPointColor(self, x, y, color):
        realX = x + 300
        realY = 300 - y
        color = self.colorMap.alloc_color(color)
        gc = self.offImage.new_gc(color)
        self.offImage.draw_point(gc, int(realX), int(realY))
        return
    
    def drawPointOffset(self, x, y, xOffset, yOffset):
        realX = 300 + (x + xOffset)
        realY = 300 - (y + yOffset)
        self.offImage.draw_point(self.gc, int(realX), int(realY))
        return
    
    def stopDrawing(self):
        self.stopFlag = True
        return
    
    def cleanAll(self):
        color = self.colorMap.alloc_color("white")
        gc = self.offImage.new_gc(color)
        self.offImage.draw_rectangle(gc, True, 0, 0, 600, 600)
        return
    
    def zoomIn(self, x0, y0, x1, y1):
        # translate computer-coordinates into standard-coordinates
        x0 = x0 - 300
        x1 = x1 - 300
        y0 = 300 - y0
        y1 = 300 - y1
        self.zoomHistory.append([x0, y0, x1, y1])
        print "111111111111111111"
        return True
    
    def zoomOut(self):
        if len(self.zoomHistory) == 0:
            return False
        self.zoomHistory.pop()
        return True
    