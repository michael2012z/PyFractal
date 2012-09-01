from Fractal import Fractal
import math
import gtk
import random

class IFSFractal (Fractal):
    ''' Formula:
        x' = ax + by + c
        y' = dx + ey + f
        Possibility  = p
    '''
    # a, b, c, d, e, f, p
    transitions = []
    startX = 0
    startY = 0
    width = 0
    height = 0
    dots = 100000
    offsetX = 0
    offsetY = 0
    
    predefinedParams = []
    
    def __init__(self):
        Fractal.__init__(self)
        self.gladefile = "fractals/IFSFractal.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        callbackDic = { "on_paramEnabled1_toggled" : self.on_paramEnabled1_toggled,
                        "on_paramEnabled2_toggled" : self.on_paramEnabled2_toggled,
                        "on_paramEnabled3_toggled" : self.on_paramEnabled3_toggled, 
                        "on_paramEnabled4_toggled" : self.on_paramEnabled4_toggled,
                        "on_paramEnabled5_toggled" : self.on_paramEnabled5_toggled,
                        "on_paramEnabled6_toggled" : self.on_paramEnabled6_toggled,
                        "on_paramEnabled7_toggled" : self.on_paramEnabled7_toggled, 
                        "on_paramEnabled8_toggled" : self.on_paramEnabled8_toggled,
                        "on_presetCombobox_changed": self.on_presetCombobox_changed }
        self.wTree.signal_autoconnect(callbackDic)
        self.definePresetParams()
        
        return
    
    def getControlPanel(self):
        return self.wTree.get_widget('controlPanel')
    
    def definePresetParams(self):
        # each preset is defined as:
        # [ [name, startX, startY, offsetX, offsetY, width, height, dots]
        #   [a, b, c, d, e, f, p]
        #   ......
        #   [a, b, c, d, e, f, p] ]
        self.predefinedParams = \
            [ [ ["IFS 1", 0, 0, -300, -270, 600, int(300*1.732), 100000],
                [0.5,     0,      0,      0,      0.5,        0,      0.333],
                [0.5,     0,      0.5,    0,      0.5,        0,      0.333],
                [0.5,     0,      0.25,   0,      0.5,        0.5,    0.334]  ] ]

        
        # append to preset combobox
        presetCombobox = self.wTree.get_widget('presetCombobox')
        for i in range(0, len(self.predefinedParams)):
            presetCombobox.append_text(self.predefinedParams[i][0][0])
        return
    
    def on_paramEnabled1_toggled(self, widget):
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'p']:
            entryName = 'param1' + i
            print entryName
            self.wTree.get_widget(entryName).set_editable(widget.get_active())
        return
    
    def on_paramEnabled2_toggled(self, widget):
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'p']:
            entryName = 'param2' + i
            print entryName
            self.wTree.get_widget(entryName).set_editable(widget.get_active())
        return
    
    def on_paramEnabled3_toggled(self, widget):
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'p']:
            entryName = 'param3' + i
            print entryName
            self.wTree.get_widget(entryName).set_editable(widget.get_active())
        return
    
    def on_paramEnabled4_toggled(self, widget):
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'p']:
            entryName = 'param4' + i
            print entryName
            self.wTree.get_widget(entryName).set_editable(widget.get_active())
        return
    
    def on_paramEnabled5_toggled(self, widget):
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'p']:
            entryName = 'param5' + i
            print entryName
            self.wTree.get_widget(entryName).set_editable(widget.get_active())
        return
    
    def on_paramEnabled6_toggled(self, widget):
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'p']:
            entryName = 'param6' + i
            print entryName
            self.wTree.get_widget(entryName).set_editable(widget.get_active())
        return
    
    def on_paramEnabled7_toggled(self, widget):
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'p']:
            entryName = 'param7' + i
            print entryName
            self.wTree.get_widget(entryName).set_editable(widget.get_active())
        return
    
    def on_paramEnabled8_toggled(self, widget):
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'p']:
            entryName = 'param8' + i
            print entryName
            self.wTree.get_widget(entryName).set_editable(widget.get_active())
        return
    
    def on_presetCombobox_changed(self, widget):
        index = widget.get_active()
        if index == 0:
            return
        
        param = self.predefinedParams[index - 1]
        self.setPredefinedParameter(param)
        return
    
    def setPredefinedParameter(self, param):
        # set startX, startY, offsetX, offsetY, width, height, dots
        self.wTree.get_widget('entryStartX').set_text(param[0][1].__str__())
        self.wTree.get_widget('entryStartY').set_text(param[0][2].__str__())
        self.wTree.get_widget('entryOffsetX').set_text(param[0][3].__str__())
        self.wTree.get_widget('entryOffsetY').set_text(param[0][4].__str__())
        self.wTree.get_widget('entryWidth').set_text(param[0][5].__str__())
        self.wTree.get_widget('entryHeight').set_text(param[0][6].__str__())
        self.wTree.get_widget('entryDots').set_text(param[0][7].__str__())
        #set formulas
        for i in range(1, len(param)):
            widgetName = 'paramEnabled' + i.__str__()
            self.wTree.get_widget(widgetName).set_active(True)
            formulaTable = ['a', 'b', 'c', 'd', 'e', 'f', 'p']
            for j in formulaTable:
                entryName = 'param' + i.__str__() + j
                self.wTree.get_widget(entryName).set_editable(True)
                self.wTree.get_widget(entryName).set_text(param[i][formulaTable.index(j)].__str__())
        #set blank transitions
        for i in range(len(param), 8):
            widgetName = 'paramEnabled' + i.__str__()
            self.wTree.get_widget(widgetName).set_active(False)
            formulaTable = ['a', 'b', 'c', 'd', 'e', 'f', 'p']
            for j in formulaTable:
                entryName = 'param' + i.__str__() + j
                self.wTree.get_widget(entryName).set_editable(False)
                self.wTree.get_widget(entryName).set_text('')
            
        return
    
    def fetchParameters (self):
        # get transitions from control panel
        self.startX = int(self.wTree.get_widget('entryStartX').get_text())
        self.startY = int(self.wTree.get_widget('entryStartY').get_text())
        self.offsetX = int(self.wTree.get_widget('entryOffsetX').get_text())
        self.offsetY = int(self.wTree.get_widget('entryOffsetY').get_text())
        self.width = int(self.wTree.get_widget('entryWidth').get_text())
        self.height = int(self.wTree.get_widget('entryHeight').get_text())
        self.dots = int(self.wTree.get_widget('entryDots').get_text())
        
        self.transitions = []
        for i in range(1, 9):
            widgetName = 'paramEnabled' + i.__str__()
            if self.wTree.get_widget(widgetName).get_active() == False:
                break;
            else:
                formulaTable = ['a', 'b', 'c', 'd', 'e', 'f', 'p']
                transitionLine = []
                for j in formulaTable:
                    entryName = 'param' + i.__str__() + j
                    transitionLine.append(float(self.wTree.get_widget(entryName).get_text()))
                self.transitions.append(transitionLine)
        
        return
    
    def checkParameters(self):
        # check number of paramers in each transition
        # check the summary of every possibility
        sum = 0.0
        for tr in self.transitions:
            if len(tr) != 7:
                print "Error: number of parameters is wrong in ", tr
                return False
            sum += tr[6]
        if sum > 1.0001 or sum < 0.9999:
            print "Error: summary of each possibility is no 1.0, but ", sum
            return False
        return True
    
    
    def drawing(self):
        self.cleanAll()
        self.fetchParameters()
        if self.checkParameters() == False:
            return
        self.stopFlag = False
        x = oldx = self.startX
        y = oldy = self.startY
        paramIndex = 0
        for i in range(0, self.dots):
            # check stop flag at beginning of each loop
            if self.stopFlag == True:
                self.stopFlag = False
                return
            # generate a random and select the corresponding parameter group
            r = random.random()
            pSum = 0.0
            for j in range(0, len(self.transitions)):
                pSum += self.transitions[j][6]
                if pSum >= r:
                    paramIndex = j
                    break;
            # choose the parameter and calculate
            a = self.transitions[paramIndex][0]
            b = self.transitions[paramIndex][1]
            c = self.transitions[paramIndex][2]
            d = self.transitions[paramIndex][3]
            e = self.transitions[paramIndex][4]
            f = self.transitions[paramIndex][5]
            x = a*oldx + b*oldy + c
            y = d*oldx + e*oldy + f
            self.drawPointOffset(self.width*x, self.height*y, self.offsetX, self.offsetY)
            oldx = x
            oldy = y
        return
    
    def getName(self):
        return "IFS"
    