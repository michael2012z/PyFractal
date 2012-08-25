from Fractal import Fractal
import gtk

class BlankFractal (Fractal):
    
    def __init__(self):
        Fractal.__init__(self)
        return
    
    def getControlPanel(self):
        self.gladefile = "fractals/BlankFractal.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        return self.wTree.get_widget('controlPanel')

    
    def drawing(self):
        self.cleanAll()
        self.drawLine(-300, -300, 300, 300)
        self.drawLine(-300, 300, 300, -300)
        return
        
    def getName(self):
        return "Blank"