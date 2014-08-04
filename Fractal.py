import gtk


class Fractal:
    zoomHistory = []
    zoomArea = (-300, -300, 300, 300)
    border = (-300, -300, 300, 300)
    paintQueue = []
    

    def __init__(self):
        print "Fractal.__init__"
        self.colorMap = gtk.gdk.colormap_get_system()
        self.color = self.colorMap.alloc_color("white")
        return
    
    def getName(self):
        return ""
    
    def drawing(self):
        return
    
    def getControlPanel(self):
        return None
    
    def drawLine(self, x1, y1, x2, y2, red, green, blue):
        realX1 = x1 + 300
        realX2 = x2 + 300
        realY1 = 300 - y1
        realY2 = 300 - y2
        self.paintQueue.append([[int(realX1), int(realY1), int(realX2), int(realY2)], [red, green, blue]])
        return
    
    def drawPoint(self, x, y, red, green, blue):
        realX = x + 300
        realY = 300 - y
        self.paintQueue.append([[int(realX), int(realY), int(realX), int(realY)], [red, green, blue]])
        return
    
    def drawPointOffset(self, x, y, xOffset, yOffset, red, green, blue):
        realX = 300 + (x + xOffset)
        realY = 300 - (y + yOffset)
        self.paintQueue.append([[int(realX), int(realY), int(realX), int(realY)], [red, green, blue]])
        return

    def getPaintQueue(self):
        return self.paintQueue

    def cleanAll(self):
        self.paintQueue = []
        return
    
    def zoomIn(self, x0, y0, x1, y1):
        # translate computer-coordinates into standard-coordinates
        x0 = x0 - 300
        x1 = x1 - 300
        y0 = 300 - y0
        y1 = 300 - y1
        self.zoomArea = (x0, y0, x1, y1)
        print "zoomArea is ", self.zoomArea
        self.zoomHistory.append(self.zoomArea)
        return True
    
    def zoomOut(self):
        if len(self.zoomHistory) == 0:
            return False
        self.zoomHistory.pop()
        return True
    
