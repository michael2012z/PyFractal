from Fractal import Fractal
import math
import gtk

class JuliaSet (Fractal):
    
    c0 = (0.75, 0.0)
    width = 600
    height = 600
    predefinedParams = []
    
    def __init__(self):
        if __name__ == "__main__":
            return
        Fractal.__init__(self)
        self.gladefile = "fractals/JuliaSetFractal.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        callbackDic = { "on_presetCombobox_changed" : self.on_presetCombobox_changed }
        self.wTree.signal_autoconnect(callbackDic)
        self.definePresetParams()
        return
    
    def getControlPanel(self):
        return self.wTree.get_widget('controlPanel')
    
    def definePresetParams(self):
        self.predefinedParams.append(["Configuration 0", 0.75, 0.0])
        self.predefinedParams.append(["Configuration 1", 0.0, 0.0])
        self.predefinedParams.append(["Configuration 2", -0.46, 0.57])
        self.predefinedParams.append(["Configuration 3", -0.595, -0.435])
        self.predefinedParams.append(["Configuration 4", -0.615, -0.43])
        self.predefinedParams.append(["Configuration 5", 0.41, -0.19])
        self.predefinedParams.append(["Configuration 6", -0.925, 0.255])
        self.predefinedParams.append(["Configuration 7", 0.4399, 0.175])
        self.predefinedParams.append(["Configuration 8", -0.74543, 0.11301])
        self.predefinedParams.append(["Configuration 9", -0.199, -0.66])
        self.predefinedParams.append(["Configuration 10", -0.135, -0.65])
        self.predefinedParams.append(["Configuration 11", 0.21, -0.555])
        self.predefinedParams.append(["Configuration 12", 0.235, -0.515])
        self.predefinedParams.append(["Configuration 13", -0.77, 0.08])
        self.predefinedParams.append(["Configuration 14", -0.41, -0.635])
        self.predefinedParams.append(["Configuration 15", -0.11, 0.6557])
        
        presetCombobox = self.wTree.get_widget('presetCombobox')
        for i in range(0, len(self.predefinedParams)):
            presetCombobox.append_text(self.predefinedParams[i][0])
        return
    
    def cPlus(self, c1, c2):
        c = ((c1[0] + c2[0]), (c1[1] + c2[1]))
        return c
    
    def cMinus(self, c1, c2):
        c = ((c1[0] - c2[0]), (c1[1] - c2[1]))
        return c
    
    def cMulti(self, c1, c2):
        re = c1[0]*c2[0] - c1[1]*c2[1]
        im = c1[1]*c2[0] + c1[0]*c2[1]
        return (re, im)
    
    def drawing(self):
        self.cleanAll()
        self.fetchParameters()
        self.stopFlag = False
        max = 0
        for i in range(-self.width/2, self.width/2):
            for j in range(-self.height/2, self.height/2):
                #print "checking point ", i, j
                z = (1.5 * i/(self.width/2), 1.5*j/(self.height/2))
                #print z
                k = 0
                for k in range(0, 64):
                    # check stop flag at beginning of each loop
                    if self.stopFlag == True:
                        self.stopFlag = False
                        return
                    if (z[0]*z[0] + z[1]*z[1]) <= 4.0:
                        # calculate new z
                        z = self.cMinus(self.cMulti(z, z), self.c0)
                        if k > max:
                            max = k
                        #print "new z: ", z
                    else:
                        break
                if True:
                    red=1.0-1.0*(k/16)
                    green=1.0-1.0*((k%16)/4)
                    blue=1.0-1.0*(k%4)
                    #color = gtk.gdk.Color(red=1.0*k/128, green=(1.0-1.0*k/128), blue=(1.0 - 1.0*k/128))
                    self.drawPoint(i, j, red, green, blue)
        print max
        return
    
    def getName(self):
        return "Julia Set"
    
    def on_presetCombobox_changed(self, widget):
        index = widget.get_active()
        if index == 0:
            return
        
        param = self.predefinedParams[index - 1]
        self.wTree.get_widget('entryCRe').set_text(param[1].__str__())
        self.wTree.get_widget('entryCIm').set_text(param[2].__str__())
        return
    
    def fetchParameters (self):
        # get parameters from control panel
        re = float(self.wTree.get_widget('entryCRe').get_text())
        im = float(self.wTree.get_widget('entryCIm').get_text())
        self.c0 = (re, im)
        print self.c0
        return
        
        
        
if __name__ == "__main__":
    julia = JuliaSet()
    z = (1.0*100/100, 0.0*100/100)
    for i in range(0, 20):
        print (z[0]*z[0] + z[1]*z[1])
        print (z[0]*z[0] + z[1]*z[1]) <=4
        z = julia.cMinus(julia.cMulti(z, z), julia.c0)
        print z
    pass
