import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import time
import threading
import gobject
from SyntaxFractal import SyntaxFractal
from BlankFractal import BlankFractal

class MainWindow:
    drawing_thread = None
    refreshing_thread = None
    wTree = None
    drawArea = None
    offImage = None
    drawingFinish = True
    selectorCombo = None
    
    fractalList = None
    
    def registerFractals(self):
        self.fractalList = []
        self.fractalList.append(SyntaxFractal())
        self.fractalList.append(BlankFractal())
        return
    
    def showWindow(self):
        # show main window
        self.gladefile = "glade/MainWindow.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        callbackDic = { "on_mainWindow_destroy" : lambda x: gtk.main_quit(),
                        "on_drawButton_clicked" : self.on_drawButton_clicked,
                        "on_drawingArea_expose_event" : self.on_drawingArea_expose_event, 
                        "on_selectorCombo_changed" : self.on_selectorCombo_changed }
        self.wTree.signal_autoconnect(callbackDic)
        self.wTree.get_widget('mainWindow').show()
        
        # make off-screen image
        self.drawArea = self.wTree.get_widget('drawingArea')
        self.offImage = gtk.gdk.Pixmap(self.drawArea.window, 600, 600, -1)
        colorMap = gtk.gdk.colormap_get_system()
        color = colorMap.alloc_color("white")
        gc = self.offImage.new_gc(color)
        self.offImage.draw_rectangle(gc, True, 0, 0, 600, 600)
        
        # make the combo box
        self.selectorCombo = self.wTree.get_widget('selectorCombo')
        #self.selectorCombo.append_text('Select a template')
        for i in range(0, len(self.fractalList)):
            self.selectorCombo.append_text(self.fractalList[i].getName())
         
        # set control panel
        self.controlPanelContainer = self.wTree.get_widget('controlPanelContainer')
        return
    
    def __init__(self):
        self.registerFractals()
        self.showWindow()
        return
    
    def on_selectorCombo_changed(self, widget):
        index = widget.get_active()
        if (index == 0) or (index > len(self.fractalList)):
            return
        fractal = self.fractalList[index - 1]
        self.drawing_thread = fractal
        
        existingComponents = self.controlPanelContainer.get_children()
        if len(existingComponents) != 0:
            self.controlPanelContainer.remove(existingComponents[0])
        self.controlPanelContainer.pack_start(self.drawing_thread.getControlPanel(), False, False, 0)
        return
        
    def on_drawButton_clicked(self, widget):
        if self.drawingFinish == False:
            return
        
        self.drawingFinish = False
        colorMap = gtk.gdk.colormap_get_system()
        color = colorMap.alloc_color("white")
        gc = self.offImage.new_gc(color)
        self.offImage.draw_rectangle(gc, True, 0, 0, 600, 600)
        
        print "on_drawButton_clicked"
        self.refreshing_thread = threading.Thread(target=self.refreshing)
        self.drawing_thread.start()
        self.refreshing_thread.start()
        #self.drawing_thread.join()
        #self.refreshing_thread.join()
        return

    def refreshing(self):
        gc = self.offImage.new_gc()
        #color = gtk.gdk.Color(red=65535, green=65535, blue=65535, pixel=0)
        #gc = self.drawArea.window.new_gc(color)
        while (True):
            time.sleep(0.01)
            self.drawArea.window.draw_drawable(gc, self.drawing_thread.getDrawable(), 0, 0, 0, 0, 600, 600)
            if self.drawingFinish == True:
                break
        return
    
    def on_drawingArea_expose_event(self, area, event):
        gc = self.offImage.new_gc()
        if self.drawing_thread != None:
            self.drawArea.window.draw_drawable(gc, self.drawing_thread.getDrawable(), 0, 0, 0, 0, 600, 600)
        return
    
if __name__ == '__main__':
    c = MainWindow()
    gobject.threads_init()
    gtk.main()
    pass