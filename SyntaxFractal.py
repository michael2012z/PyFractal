from Fractal import Fractal
import math
import time
import gtk

class SyntaxFractal (Fractal):
    
    delta = 0
    startingAction = []
    formulaF = []
    formulaX = []
    formulaY = []
    formulaZ = []
    fullSyntax = []
    depth = 0
    stepLength = 1
    
    def __init__(self):
        Fractal.__init__(self)
        print "SyntaxFractal.__init__"
        self.delta = 60
        self.depth = 5
        self.startingAction = ['F', '-',  '-', 'F', '-',  '-', 'F']
        self.formulaF = ['F', '+', 'F', '-',  '-', 'F', '+', 'F']
        return
    
    def getControlPanel(self):
        self.gladefile = "fractals/Syntax.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        return self.wTree.get_widget('controlPanel')
    
    def generateFullSyntax(self):
        self.fullSyntax = self.startingAction
        for i in range(0, self.depth):
            tmpSyntax = []
            for j in range(0, len(self.fullSyntax)):
                if self.fullSyntax[j] == "F":
                    tmpSyntax.extend(self.formulaF)
                elif self.fullSyntax[j] == "X":
                    tmpSyntax.extend(self.formulaX)
                elif self.fullSyntax[j] == "Y":
                    tmpSyntax.extend(self.formulaY)
                elif self.fullSyntax[j] == "Z":
                    tmpSyntax.extend(self.formulaZ)
                elif self.fullSyntax[j] == "+" or \
                     self.fullSyntax[j] == "-" or \
                     self.fullSyntax[j] == "[" or \
                     self.fullSyntax[j] == "]" :
                    tmpSyntax.extend(self.fullSyntax[j])
                else:
                    print "ERROR: unrecognized symbol"
            self.fullSyntax = tmpSyntax
        return
    
    def run(self):
        direction = 0
        angle = 0.0
        oldX = -200.0
        oldY = 100.0
        newX = 0.0
        newY = 0.0
        self.generateFullSyntax()
        for i in range(0, len(self.fullSyntax)):
            time.sleep(0.001)
            if self.fullSyntax[i] == "F":
                newX = oldX + self.stepLength * math.cos(angle)
                newY = oldY + self.stepLength * math.sin(angle)
                self.drawLine(oldX, oldY, newX, newY)
                print "draw a line for (%f, %f) to (%f, %f)" %(oldX, oldY, newX, newY)
                oldX = newX
                oldY = newY
            elif self.fullSyntax[i] == "+":
                direction += self.delta
                direction %= 360
                angle = math.pi * direction / 180
                print "turn + ", self.delta
            elif self.fullSyntax[i] == "-":
                direction -= self.delta
                direction %= 360
                angle = math.pi * direction / 180
                print "turn - ", self.delta
            else:
                print "do nothing for : ", self.fullSyntax[i]
        return
        
    def __str__ (self):
        str = 'SyntaxFractal: \n'
        str += "%s%d%s" %('delta : ', self.delta, '\n')
        str += "%s%s%s" %('startingAction : ', self.startingAction, '\n')
        str += "%s%d%s" %('depth : ', self.depth, '\n')
        str += "%s%d%s" %('stepLength : ', self.stepLength, '\n')
        str += "%s%s%s" %('formulaF : ', self.formulaF, '\n')
        if len(self.formulaX) != 0:
            str += "%s%s%s" %('formulaX : ', self.formulaX, '\n')
        if len(self.formulaY) != 0:
            str += "%s%s%s" %('formulaY : ', self.formulaY, '\n')
        if len(self.formulaZ) != 0:
            str += "%s%s%s" %('formulaZ : ', self.formulaZ, '\n')
        str += "%s%s%s" %('fullSyntax : ', self.fullSyntax, '\n')
        return str
        
if __name__ == '__main__':
    syntax = SyntaxFractal()
    syntax.delta = 60
    syntax.depth = 3
    syntax.startingAction = ['F']
    syntax.formulaF = ['F', '+', 'F', '-', 'F']
    syntax.generateFullSyntax()
    #print syntax
    syntax.run()
    pass
