from mymapapi import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton 
from PyQt5.QtWidgets import QComboBox, QLineEdit
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
            self.x_step = 360 / 2 ** self.zooming * 1.76
            self.y_step = 180 / 2 ** self.zooming * 2
            
            if e.key() == Qt.Key_PageUp:
                if self.zooming < 19:
                    self.zooming += 1
                    self.show_map_file()
            elif e.key() == Qt.Key_PageDown:
                if self.zooming > 0:
                    self.zooming -= 1
                    self.show_map_file()
                    
            elif e.key() == Qt.Key_Down:
                coord = float(self.lat_input.text()) - self.y_step
                if coord < -85:
                    coord = -85
                self.lat_input.setText(str(coord))
                self.show_map_file()
                
            elif e.key() == Qt.Key_Up:
                coord = float(self.lat_input.text()) + self.y_step
                if coord > 85:
                    coord = 85
                self.lat_input.setText(str(coord))
                self.show_map_file()    
                
            elif e.key() == Qt.Key_Right:
                coord = float(self.lon_input.text()) + self.x_step
                if coord > 180:
                    coord = -(180 - self.x_step)
                self.lon_input.setText(str(coord))
                self.show_map_file()   
                
            elif e.key() == Qt.Key_Left:
                coord = float(self.lon_input.text()) - self.x_step
                if coord < -180:
                    coord = 180 - self.x_step                
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

        self.label.mousePressEvent = self.get_pos

        self.type_layout.addItems(["Схема", "Спутник", "Гибрид"])
        self.type_layout.activated[str].connect(self.change_type)

        self.index.clicked.connect(self.change_index)

        self.start.clicked.connect(self.show_map_file)
        self.clear.clicked.connect(self.clear_mark)
             
        self.layout = "map"
        self.zooming = 8
        self.mark = False
        self.x_step = (360 / 2 ** self.zooming) * 2
        self.y_step = (180 / 2 ** self.zooming) * 2


    def get_pos(self, event):
        button = event.button()
        self.x_step = (360 / 2 ** self.zooming) * 1.76
        self.y_step = (180 / 2 ** self.zooming) * 2            
        x, y = event.pos().x() - 225, event.pos().y() - 225
        x = float(self.lon_input.text()) + self.x_step / 450 * x
        y = float(self.lat_input.text()) - self.y_step / 450 * y

        if button == Qt.LeftButton:
            self.clear_mark()
            self.mark = [x, y]
            self.obj = geocode('{},{}'.format(x, y))
            self.address.setPlainText(self.exist_check())            
            self.show_map_file()
        elif button == Qt.RightButton:
            result = find_org('{},{}'.format(x, y), '0.00045,0.00045', None, {"rspn": "1"})
            if result and lonlat_distance(result[0]['geometry']['coordinates'], (x, y)) > 50:
                self.org = result
                self.clear_mark() 
                self.mark = [x, y] 
                self.address.setPlainText(self.exist_check()) 
                self.show_map_file()
            

    def change_index(self, state):
        if self.address.toPlainText():
            self.address.setPlainText(self.exist_check())


    def exist_check(self):

        address = self.obj["metaDataProperty"]["GeocoderMetaData"]["text"] if "metaDataProperty" in self.obj else \
                  self.obj['properties']['CompanyMetaData']["address"]

        if "metaDataProperty" in self.obj and "postal_code" in self.obj["metaDataProperty"]["GeocoderMetaData"]["Address"]:
            index = self.obj["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
        elif "properties" in self.obj and "postalCode" in self.obj['properties']['CompanyMetaData']:
            index = self.obj['properties']['CompanyMetaData']["postalCode"]
        else:
            index = ""

        return "{}. Индекс: {}".format(address, index)
 

    def change_type(self, type_map):
        self.layout = {"Схема": "map", "Спутник": "sat", "Гибрид": "skl"}[type_map]
        self.show_map_file()


    def clear_mark(self):
        self.mark = False
        self.address.setPlainText("")
        self.show_map_file()
        

    def show_map_file(self):
        try:
            if self.sender() is not None and type(self.sender()) != type(self.type_layout) and self.sender().text() == "Искать":
                self.zooming = 19
                self.obj = geocode(self.search.text())
                self.address.setPlainText(self.exist_check())
                self.mark = self.obj["Point"]["pos"].split() if "Point" in self.obj else self.obj['geometry']['coordinates']
                self.lat_input.setText(str(self.mark[1]))
                self.lon_input.setText(str(self.mark[0]))
                self.search.setText("")
      
            params = {"ll": ",".join([self.lon_input.text(),self.lat_input.text()]),
                      "l": self.layout,
                      "z": str(self.zooming),
                      "size": "450,450"}

            if self.mark:
                params["pt"] = "{},{}".format(*self.mark) + ",pm2bll"
                
            f_name = get_file_map(params)
        
            if f_name:
                self.image = f_name

            self.qimage = ImageQt(self.image)
            self.pixmap = QPixmap(QPixmap.fromImage(self.qimage))
            self.label.setPixmap(self.pixmap)
            self.show()

        except Exception as e:
            print(e)
     
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


