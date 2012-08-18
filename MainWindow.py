import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import time
import threading
import gobject

class MainWindow:
    drawing_thread = None
    refreshing_thread = None
    wTree = None
    drawArea = None
    offImage = None
    drawingFinish = True
    
    def __init__(self):
        self.gladefile = "glade/MainWindow.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        callbackDic = { "on_mainWindow_destroy" : lambda x: gtk.main_quit(),
                        "on_drawButton_clicked" : self.on_drawButton_clicked,
                        "on_drawingArea_expose_event" : self.on_drawingArea_expose_event }
        self.wTree.signal_autoconnect(callbackDic)
        self.wTree.get_widget('mainWindow').show()
        self.drawArea = self.wTree.get_widget('drawingArea')
        self.offImage = gtk.gdk.Pixmap(self.drawArea.window, 600, 600, -1)
        colorMap = gtk.gdk.colormap_get_system()
        color = colorMap.alloc_color("white")
        gc = self.offImage.new_gc(color)
        self.offImage.draw_rectangle(gc, True, 0, 0, 600, 600)
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
        self.drawing_thread = threading.Thread(target=self.drawing)
        self.refreshing_thread = threading.Thread(target=self.refreshing)
        self.drawing_thread.start()
        self.refreshing_thread.start()
        #self.drawing_thread.join()
        #self.refreshing_thread.join()
        return
    
    def drawing(self):
        colorMap = gtk.gdk.colormap_get_system()
        color = colorMap.alloc_color(gtk.gdk.Color(0, 0, 65535))
        gc = self.offImage.new_gc(color)
        for i in range(0, 600):
            for j in range(0, 600):
                self.offImage.draw_point(gc, i, j)
        self.drawingFinish = True
        return

    def refreshing(self):
        gc = self.offImage.new_gc()
        #color = gtk.gdk.Color(red=65535, green=65535, blue=65535, pixel=0)
        #gc = self.drawArea.window.new_gc(color)
        while (True):
            time.sleep(0.01)
            self.drawArea.window.draw_drawable(gc, self.offImage, 0, 0, 0, 0, 600, 600)
            if self.drawingFinish == True:
                break
        return
    
    def on_drawingArea_expose_event(self, area, event):
        gc = self.offImage.new_gc()
        self.drawArea.window.draw_drawable(gc, self.offImage, 0, 0, 0, 0, 600, 600)
        return
    
if __name__ == '__main__':
    c = MainWindow()
    gobject.threads_init()
    gtk.main()
    pass