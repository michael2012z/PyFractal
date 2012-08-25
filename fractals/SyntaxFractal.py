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
    predefinedParams = []
    stopFlag = False
    
    def __init__(self):
        Fractal.__init__(self)
        print "SyntaxFractal.__init__"
        self.gladefile = "fractals/SyntaxFractal.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        callbackDic = { "on_checkbutton1_toggled" : self.on_checkbutton1_toggled,
                        "on_checkbutton2_toggled" : self.on_checkbutton2_toggled,
                        "on_checkbutton3_toggled" : self.on_checkbutton3_toggled, 
                        "on_presetCombobox_changed" : self.on_presetCombobox_changed }
        self.wTree.signal_autoconnect(callbackDic)
        self.definePresetParams()
        return
    
    def definePresetParams(self):
        # each preset is defined as:
        # [name, initial angle, initial action, depth, step length, delta, F, X enabled, X, Y enabled, Y, Z enabled, Z, startX, startY]
        self.predefinedParams.append(["Koch Snowflake", 0, "F--F--F", 5, 2, 60, "F+F--F+F", False, "", False, "", False, "", -250, 150])
        self.predefinedParams.append(["Koch R-Snowflake", 0, "F++F++F", 5, 2, 60, "F+F--F+F", False, "", False, "", False, "", -250, -150])
        self.predefinedParams.append(["C 1 1", 0, "F+F+F+F", 4, 1, 90, "F+F-F-F+F+F-F", False, "", False, "", False, "", 0, -150])
        self.predefinedParams.append(["C 1 2", 0, "F-F-F-F-", 4, 2, 90, "FF-F-F-F-F-F+F", False, "", False, "", False, "", 200, 200])
        self.predefinedParams.append(["C 2 1", 90, "F", 6, 2, 25, "F[+F]F[-F+F]", False, "", False, "", False, "", 0, -200])
        self.predefinedParams.append(["C 2 2", 90, "F", 5, 5, 20, "FF+[+F-F-F]-[-F+F+F]", False, "", False, "", False, "", 200, -200])
        self.predefinedParams.append(["C 2 3", 55, "F", 7, 3, 25, "F[-F][+F]F", False, "", False, "", False, "", 0, -200])
        self.predefinedParams.append(["C 2 4", 0, "F-F-F-F", 5, 2, 90, "F[F]-F+F[--F]+F-F", False, "", False, "", False, "", -250, 250])
        self.predefinedParams.append(["C 2 5", 0, "F-F-F-F", 5, 2, 90, "FF[-F-F-F]F", False, "", False, "", False, "", -100, -200])
        self.predefinedParams.append(["C 3 1", 0, "X", 3, 3, 90, "F", True, "-YF+XFX+FY-", True, "+XF-YFY-FX+", False, "", 0, 0])
        
        presetCombobox = self.wTree.get_widget('presetCombobox')
        for i in range(0, len(self.predefinedParams)):
            presetCombobox.append_text(self.predefinedParams[i][0])
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
        self.stopFlag = False
        for i in range(0, len(self.fullSyntax)):
            # check stop flag at beginning of each loop
            if self.stopFlag == True:
                self.stopFlag = False
                return
            #time.sleep(0.001)
            if self.fullSyntax[i] == "F":
                newX = oldX + self.stepLength * math.cos(angle)
                newY = oldY + self.stepLength * math.sin(angle)
                self.drawLine(oldX, oldY, newX, newY)
                #print "draw a line for (%f, %f) to (%f, %f)" %(oldX, oldY, newX, newY)
                oldX = newX
                oldY = newY
            elif self.fullSyntax[i] == "+":
                direction += self.delta
                direction %= 360
                angle = math.pi * direction / 180
                #print "turn + ", self.delta
            elif self.fullSyntax[i] == "-":
                direction -= self.delta
                direction %= 360
                angle = math.pi * direction / 180
                #print "turn - ", self.delta
            elif self.fullSyntax[i] == "[":
                # save location and direction
                stack.append([oldX, oldY, direction])
            elif self.fullSyntax[i] == "]":
                # pop location and direction
                oldX, oldY, direction = stack.pop()
            else:
                print "do nothing for : ", self.fullSyntax[i]
        return
    
    def stopDrawing(self):
        self.stopFlag = True
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
    
    def on_presetCombobox_changed(self, widget):
        index = widget.get_active()
        if index == 0:
            return
        
        param = self.predefinedParams[index - 1]
        self.wTree.get_widget('entry1').set_text(param[1].__str__())
        self.wTree.get_widget('entry2').set_text(param[2])
        self.wTree.get_widget('entry3').set_text(param[3].__str__())
        self.wTree.get_widget('entry4').set_text(param[4].__str__())
        self.wTree.get_widget('entry5').set_text(param[5].__str__())
        self.wTree.get_widget('entry6').set_text(param[6])
        self.wTree.get_widget('checkbutton1').set_active(param[7])
        self.wTree.get_widget('entry7').set_text(param[8])
        self.wTree.get_widget('checkbutton2').set_active(param[9])
        self.wTree.get_widget('entry8').set_text(param[10])
        self.wTree.get_widget('checkbutton3').set_active(param[11])
        self.wTree.get_widget('entry9').set_text(param[12])
        self.wTree.get_widget('entry10').set_text(param[13].__str__())
        self.wTree.get_widget('entry11').set_text(param[14].__str__())
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
