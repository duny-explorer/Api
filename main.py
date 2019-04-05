from mymapapi import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton 
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL.ImageQt import ImageQt
from PyQt5 import uic


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.initUI()
    
    def keyPressEvent(self, e):
        try:
            if e.key() == Qt.Key_PageUp:
                if self.zooming < 19:
                    self.zooming += 1
                    self.show_map_file()
            elif e.key() == Qt.Key_PageDown:
                if self.zooming > 0:
                    self.zooming -= 1
                    self.show_map_file()
        except Exception as e:
            print(e)
    
 
    def initUI(self):
        self.setWindowTitle('Карта')
        self.image = Image.open("one.png")
        self.btn.clicked.connect(self.show_map_file)

        self.pixmap = QPixmap.fromImage(ImageQt(self.image))
        self.label.setPixmap(self.pixmap)
             
        self.count = 0
        self.zooming = 8

 
    def show_map_file(self):
        lon = self.lon_input.text()
        lat = self.lat_input.text()

        try:
            f_name = get_file_map({"ll": ",".join([lon,lat]),
                               "l": "map",
                               "z": str(self.zooming),
                               "size": "450,450"})
        except Exception:
            print(e)
        
        if f_name:
            self.image = f_name

        self.qimage = ImageQt(self.image)
        self.pixmap = QPixmap(QPixmap.fromImage(self.qimage))
        self.label.setPixmap(self.pixmap)
        self.show()
     
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

