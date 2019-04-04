from mymapapi import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton 
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
 
W = 400
H = 450
dMenu = 50
m = 10 #отступ
map_w, map_h = W -2 * m, H - dMenu - 2 * m


class Example(QWidget):
    def __init__(self):
        super().__init__()
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
        self.setGeometry(100, 100, W, H)
        self.setWindowTitle('Карта')

        self.maps = "one.png"
         
        self.btn = QPushButton('Отобразить', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(W //3 * 2, 30)
        self.btn.clicked.connect(self.show_map_file)
 
        self.label = QLabel(self)
        self.label.setText("Введите координаты центра карты:")
        self.label.move(10, 10)
 
        self.lat_input = QLineEdit(self)
        self.lat_input.move(10, 30)
        self.lat_input.setText("55.7507")
        self.lon_input = QLineEdit(self)
        self.lon_input.move(W //3 * 1, 30)
        self.lon_input.setText("37.6256")

        self.pixmap = QPixmap(self.maps)
        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)
        self.lbl.setGeometry(m , m + dMenu, map_w, map_h)
        self.lbl.move(10, 60)
         
        self.count = 0
        self.zooming = 0  # зум 
 
    def show_map_file(self):
        # Показать карту
        lon = self.lon_input.text()
        lat = self.lat_input.text()
        
        map_locations = "ll=" + ",".join([lon,lat])# + "&spn=1.0,1.0"
                
        map_type = "map"
        map_param = "z={}&size=400,400".format(self.zooming)
        f_name = get_file_map(map_locations, map_type,map_param)
        if f_name:
            self.maps = f_name
        
        self.pixmap.load(self.maps)
        self.lbl.setPixmap(self.pixmap)
        
     
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
