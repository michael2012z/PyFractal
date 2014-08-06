from Fractal import Fractal
import math
import gtk
import random

class DLA (Fractal):
    maxImageRadius = 300
    escapeBandWidth = 200
    maxTry = 10000
    map = []
    
    def __init__(self):
        Fractal.__init__(self)
        self.gladefile = "fractals/DLAFractal.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        for i in range(600):
            self.map.append([])
            for j in range(600):
                self.map[i].append(False)
        return
    
    def getControlPanel(self):
        return self.wTree.get_widget('controlPanel')

    def getInitPosition(self, imageRadius):
        distance = imageRadius + random.random() * self.escapeBandWidth
        angle = 2 * math.pi * random.random()
        x = distance * math.cos(angle)
        y = distance * math.sin(angle)        
        return int(x), int(y)

    def randomMove(self, x, y):
        if random.random() > 0.5:
            x = x + 1
        else:
            x = x - 1
        if random.random() > 0.5:
            y = y + 1
        else:
            y = y - 1
        return x, y

    def calcDistance(self, x, y):
        return math.sqrt(x*x + y*y)

    def adhibited(self, x, y):
        for i in [x-1, x, x+1]:
            for j in [y-1, y, y+1]:
                if self.map[i+300][j+300] == True:
                    return True
        return False
        

    def drawing(self):
        self.cleanAll()
        self.stopFlag = False
        for i in range(600):
            for j in range(600):
                self.map[i][j] = False

        self.map[300][300] = True
        self.drawPoint(0, 0, 0.0, 0.0, 0.0)
        imageRadius = 1
        dots = 0
        while imageRadius <= self.maxImageRadius:
            dots = dots + 1
            if (dots % 1000) == 0 :
                print dots
            x, y = self.getInitPosition(imageRadius)
            for i in range(self.maxTry):
                if self.stopFlag == True:
                    self.stopFlag = False
                    return
                x, y = self.randomMove(x, y)
                distance = self.calcDistance(x, y)
                if distance > imageRadius + self.escapeBandWidth:
                    # the seed escaped, ignore it
                    #print "escape: " + "(" + str(x) + ", " + str(y) + ")"
                    break
                elif (x <= -300 or x >= 299) or (y <= -300 or y >= 299):
                    # not in map, go on moving
                    continue
                else:
                    # in the map
                    if self.adhibited(x, y):
                        #print "adhibited: " + "(" + str(x) + ", " + str(y) + ")"
                        self.map[x+300][y+300] = True
                        if distance > imageRadius:
                            imageRadius = distance
                        self.drawPoint(x, y, 0.0, 0.0, 0.0)
                        break
                    else:
                        continue
    
    def getName(self):
        return "DLA"
    
