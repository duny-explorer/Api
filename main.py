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
            x_step = 360 / 2 ** self.zooming * 2
            y_step = 180 / 2 ** self.zooming * 2
            if e.key() == Qt.Key_PageUp:
                if self.zooming < 19:
                    self.zooming += 1
                    self.show_map_file()
            elif e.key() == Qt.Key_PageDown:
                if self.zooming > 0:
                    self.zooming -= 1
                    self.show_map_file()
                    
            elif e.key() == Qt.Key_Down:
                coord = float(self.lat_input.text()) - y_step
                if coord < -85:
                    coord = -85
                self.lat_input.setText(str(coord))
                self.show_map_file()
                
            elif e.key() == Qt.Key_Up:
                coord = float(self.lat_input.text()) + y_step
                if coord > 85:
                    coord = 85
                self.lat_input.setText(str(coord))
                self.show_map_file()    
                
            elif e.key() == Qt.Key_Right:
                coord = float(self.lon_input.text()) + x_step
                if coord > 180:
                    coord = -(180 - x_step)
                self.lon_input.setText(str(coord))
                self.show_map_file()   
                
            elif e.key() == Qt.Key_Left:
                coord = float(self.lon_input.text()) - x_step
                if coord < -180:
                    coord = 180 - x_step                
                self.lon_input.setText(str(coord))
                self.show_map_file()            
            
                
        except Exception as e:
            print(e)
    
 
    def initUI(self):
        self.setWindowTitle('Карта')
        self.image = Image.open("one.png")
        self.btn.clicked.connect(self.show_map_file)

        self.pixmap = QPixmap.fromImage(ImageQt(self.image))
        self.label.setPixmap(self.pixmap)

        self.type_layout.addItems(["Схема", "Спутник", "Гибрид"])
        self.type_layout.activated[str].connect(self.change_type)

        self.start.clicked.connect(self.show_map_file)
             
        self.layout = "map"
        self.zooming = 8
        self.ll = "55.7507, 37.6256"
        self.mark = False


    def change_type(self, type_map):
        self.layout = {"Схема": "map", "Спутник": "sat", "Гибрид": "skl"}[type_map]
        self.show_map_file()  
        

 
    def show_map_file(self):
        try:
            if self.sender().text() == "Искать":
                self.zooming = 19
                self.mark = True
                self.ll = get_coord(self.search.text())
                print(00)
        
            elif self.sender().text() == "Показать":
                lon = self.lon_input.text()
                lat = self.lat_input.text()
                self.ll = ",".join([lon,lat])
            print(00) 
            params = {"ll": self.ll,
                      "l": self.layout,
                      "z": str(self.zooming),
                      "size": "450,450"}
            print(00)
            if self.mark:
                params["pt"] = self.ll + ",pm2blywm"
         
            f_name = get_file_map(params)
        except Exception as e:
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

