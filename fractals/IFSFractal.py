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
                [0.5,     0,      0.25,   0,      0.5,        0.5,    0.334]  ],
             
              [ ["IFS 2", 0, 0, -285, -270, 600, int(300*1.732), 100000],
                [0.5, 0, 0, 0, 0.5, 0, 0.333],
                [0.5, 0, 0.5, 0, 0.5, 0, 0.333],
                [0.5, 0, 0, 0, 0.5, 0.5, 0.334] ],
                
              [ ["IFS 3", 0, 0, -300, 0, 600, 600, 100000],
                [0.333, 0, 0, 0, 0.333, 0, 0.25],
                [0.167, -0.289, 0.333, 0.289, 0.167, 0, 0.25],
                [0.167, 0.289, 0.5, -0.289, 0.167, 0.289, 0.25],
                [0.333, 0, 0.667, 0, 0.333, 0, 0.25] ],
                
              [ ["IFS 4", 0, 0, -140, -100, 280, 280, 300000],
                [0.5, -0.5, 0, 0.5, 0.5, 0, 0.5],
                [0.5, 0.5, 0.5, -0.5, 0.5, 0.5, 0.5] ],
                
              [ ["IFS 5", 0, 0, 0, -200, 300, 300, 100000],
                [0.25, 0, 0, 0, 0.5, 0, 0.154],
                [0.5, 0, -0.25, 0, 0.5, 0.5, 0.307],
                [-0.25, 0, 0.25, 0, -0.25, 1, 0.078],
                [0.5, 0, 0, 0, 0.5, 0.75, 0.307],
                [0.5, 0, 0.5, 0, -0.25, 1.25, 0.154] ],
                
              [ ["IFS 6", 0, 0, 0, -200, 40, 50, 300000],
                [0.787879, -0.424242, 1.758647, 0.242424, 0.859848, 1.408065, 0.9],
                [-0.121212, 0.257576, -6.721654, 0.05303, 0.05303, 1.377236, 0.05],
                [0.181818, -0.136364, 6.086107, 0.090909, 0.181818, 1.568035, 0.05] ],
                
              [ ["IFS 7", 0, 0, -250, -250, 500, 500, 100000],
                [0.382, 0, 0.3072, 0, 0.382, 0.619, 0.2],
                [0.382, 0, 0.6033, 0, 0.382, 0.4044, 0.2],
                [0.382, 0, 0.0139, 0, 0.382, 0.4044, 0.2],
                [0.382, 0, 0.1253, 0, 0.382, 0.0595, 0.2],
                [0.382, 0, 0.492, 0, 0.382, 0.0595, 0.2] ],
                
              [ ["IFS 8", 0, 0, 0, -150, 40, 40, 100000],
                [0.745455, -0.459091, 1.460279, 0.406061, 0.887121, 0.691072, 0.912675],
                [-0.424242, -0.065152, 3.809567, -0.175758, -0.218182, 6.741476, 0.087325] ],
                
              [ ["IFS 9", 0, 0, 0, -200, 40, 40, 300000],
                [0.824074, 0.281482, -1.88229, -0.212346, 0.864198, -0.110607, 0.8],
                [0.088272, 0.520988, 0.78536, -0.463889, -0.377778, 8.095795, 0.2] ],
                
                
              [ ["IFS 10", 0, 0, 0, -100, 100, 100, 500000],
                [-0.004, 0, -0.12, -0.19, -0.47, 0.3, 0.25],
                [0.65, 0, 0.06, 0, 0.56, 1.56, 0.25],
                [0.41, 0.46, 0.46, -0.39, 0.61, 0.4, 0.25],
                [0.52, -0.35, -0.48, 0.25, 0.74, 0.38, 0.25] ],
                
              [ ["IFS 11", 0, 0, -150, -300, 300, 200, 300000],
                [0.6, 0, 0.18, 0, 0.6, 0.36, 0.25],
                [0.6, 0, 0.18, 0, 0.6, 1.12, 0.25],
                [0.4, 0.3, 0.27, -0.3, 0.4, 0.36, 0.25],
                [0.4, -0.3, 0.27, 0.3, 0.4, 0.09, 0.25] ],
                
              [ ["IFS 12", 0, 0, 0, -250, 100, 90, 100000],
                [0, 0, 0, 0, 0.25, -0.14, 0.02],
                [0.85, 0.02, 0, -0.02, 0.83, 1, 0.84],
                [0.09, -0.28, 0, 0.3, 0.11, 0.6, 0.07],
                [-0.09, 0.28, 0, 0.3, 0.09, 0.7, 0.07] ],
                
              [ ["IFS 13", 0, 0, -250, -200, 500, 500, 200000],
                [0.195, -0.488, 0.4431, 0.344, 0.443, 0.2452, 0.25],
                [0.462, 0.414, 0.2511, -0.252, 0.361, 0.5692, 0.25],
                [-0.058, -0.07, 0.5976, 0.453, -0.111, 0.0969, 0.25],
                [-0.035, 0.07, 0.4884, -0.469, -0.022, 0.5069, 0.2],
                [-0.637, 0, 0.8562, 0, 0.501, 0.2513, 0.05] ],
                
              [ ["IFS 14", 0, 0, 0, -270, 55, 55, 500000],
                [0, 0, 0, 0, 0.16, 0, 0.01],
                [0.85, 0.04, 0, -0.04, 0.85, 1.6, 0.85],
                [0.2, -0.26, 0, 0.23, 0.22, 1.6, 0.07],
                [-0.15, 0.28, 0, 0.26, 0.24, 0.44, 0.07] ] ]

        
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
            self.drawPointOffset(self.width*x, self.height*y, self.offsetX, self.offsetY, 0, 0, 0)
            #print "drawing dot at", self.width*x, self.height*y, self.offsetX, self.offsetY
            oldx = x
            oldy = y
        return
    
    def getName(self):
        return "IFS"
    
