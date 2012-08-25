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
    formulaXEnabled = False
    formulaYEnabled = False
    formulaZEnabled = False
    fullSyntax = []
    depth = 0
    stepLength = 1
    startX = 0
    startY = 0
    
    def __init__(self):
        Fractal.__init__(self)
        print "SyntaxFractal.__init__"
        self.gladefile = "fractals/SyntaxFractal.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        callbackDic = { "on_checkbutton1_toggled" : self.on_checkbutton1_toggled,
                        "on_checkbutton2_toggled" : self.on_checkbutton2_toggled,
                        "on_checkbutton3_toggled" : self.on_checkbutton3_toggled }
        return
    
    def getControlPanel(self):
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
    
    def drawing(self):
        self.cleanAll()
        self.fetchParameters()
        if self.checkParameters() == False:
            print "Error, parameters error."
            return
        self.generateFullSyntax()
        direction = self.startingAngel
        angle = 0.0
        oldX = self.startX
        oldY = self.startY
        newX = 0.0
        newY = 0.0
        stack = []
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
            elif self.fullSyntax[i] == "[":
                # save location and direction
                stack.append([oldX, oldY, direction])
            elif self.fullSyntax[i] == "]":
                # pop location and direction
                oldX, oldY, direction = stack.pop()
            else:
                print "do nothing for : ", self.fullSyntax[i]
        return
    
    def stringToList(self, sstr):
        llist = []
        for i in range(0, len(sstr)):
            llist.extend(sstr[i])
        return llist
        
    def fetchParameters (self):
        # get parameters from control panel
        self.startingAngel = int(self.wTree.get_widget('entry1').get_text())
        self.startingAction = self.wTree.get_widget('entry2').get_text()
        self.depth = int(self.wTree.get_widget('entry3').get_text())
        self.stepLength = int(self.wTree.get_widget('entry4').get_text())
        self.delta = int(self.wTree.get_widget('entry5').get_text())
        self.formulaF = self.stringToList(self.wTree.get_widget('entry6').get_text())
        self.formulaX = self.stringToList(self.wTree.get_widget('entry7').get_text())
        self.formulaY = self.stringToList(self.wTree.get_widget('entry8').get_text())
        self.formulaZ = self.stringToList(self.wTree.get_widget('entry9').get_text())
        self.startX = int(self.wTree.get_widget('entry10').get_text())
        self.startY = int(self.wTree.get_widget('entry11').get_text())
        self.formulaXEnabled = self.wTree.get_widget('checkbutton1').get_active()
        self.formulaYEnabled = self.wTree.get_widget('checkbutton2').get_active()
        self.formulaZEnabled = self.wTree.get_widget('checkbutton3').get_active()
        return
    
    def checkFormula(self, formula):
        # examine a formula
        stack = []
        for i in range(0, len(formula)):
            if formula[i] == 'F' or formula[i] == '+' or formula[i] == '-':
                continue
            elif formula[i] == 'X' and self.formulaXEnabled == False:
                print "Error, formula X is not enabled"
                return False
            elif formula[i] == 'Y' and self.formulaYEnabled == False:
                print "Error, formula Y is not enabled"
                return False
            elif formula[i] == 'Z' and self.formulaZEnabled == False:
                print "Error, formula Z is not enabled"
                return False
            elif formula[i] == '[':
                stack.append(formula[i])
            elif formula[i] == ']':
                if len(stack) == 0:
                    print "Error, brackets doesn't match"
                    return False
                else:
                    stack.pop()
            else:
                print "Error, unknown symbol", formula[i]
                return False
        if len(stack) != 0:
            print "Error, brackets doesn't match"
            return False
        return True
        
    def checkParameters(self):
        # examine each formula
        if self.checkFormula(self.formulaF) == False:
            return False
        if self.formulaXEnabled == True and self.checkFormula(self.formulaX) == False:
            return False
        if self.formulaYEnabled == True and self.checkFormula(self.formulaY) == False:
            return False
        if self.formulaZEnabled == True and self.checkFormula(self.formulaZ) == False:
            return False
        return True
    
    def on_checkbutton1_toggled(self, widget):
        self.wTree.get_widget('entry7').set_editable(widget.get_active())
        return

    def on_checkbutton2_toggled(self, widget):
        self.wTree.get_widget('entry8').set_editable(widget.get_active())
        return

    def on_checkbutton3_toggled(self, widget):
        self.wTree.get_widget('entry9').set_editable(widget.get_active())
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
        
    def getName(self):
        return "Syntax"
    
    
    
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
