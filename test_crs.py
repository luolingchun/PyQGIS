# -*- coding: utf-8 -*-
# @Author llc
# @Date 2020/4/1 11:10
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel
from qgis.core import QgsProject, QgsCoordinateReferenceSystem, QgsApplication, QgsVectorLayer, QgsRectangle
from qgis.gui import QgsMapCanvas


class MoveThread(QThread):
    degreeSignal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MoveThread, self).__init__(parent)

    def run(self) -> None:
        for i in range(180):
            self.degreeSignal.emit(i)
            time.sleep(0.1)


class MyApp(QDialog):
    def __init__(self, parent=None):
        super(MyApp, self).__init__()
        self.vl = QVBoxLayout(self)
        self.pushbuttonStart = QPushButton("start", self)
        self.vl.addWidget(self.pushbuttonStart)

        self.label = QLabel(self)
        self.vl.addWidget(self.label)

        self.mapCanvas = QgsMapCanvas()
        self.mapCanvas.setCanvasColor(QColor(0, 0, 0))
        self.vl.addWidget(self.mapCanvas)

        self.pushbuttonStart.clicked.connect(self.add_layer)
        self.mapCanvas.xyCoordinates.connect(lambda p: self.label.setText(str(p.x()) + ', ' + str(p.y())))

    def add_layer(self):
        QgsProject.instance().removeAllMapLayers()

        shp = r"world.shp"
        layer = QgsVectorLayer(shp, "shp", "ogr")
        QgsProject.instance().addMapLayer(layer)
        self.mapCanvas.setLayers([layer])

        # crsSrc = QgsCoordinateReferenceSystem("EPSG:4326")
        # crsDest = QgsCoordinateReferenceSystem("EPSG:3857")
        crsDest = QgsCoordinateReferenceSystem(
            "PROJ:+proj=ortho +lat_0=0 +lon_0=100 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs")

        QgsProject.instance().setCrs(crsDest)
        self.mapCanvas.setDestinationCrs(crsDest)
        self.mapCanvas.setExtent(QgsRectangle(-6378137, -6378137, 6378137, 6378137))
        self.mapCanvas.refresh()

        self.set_crs()

    def set_crs(self):
        self.moveThread = MoveThread(self)
        self.moveThread.degreeSignal.connect(self.process_signal)
        self.moveThread.start()

    def process_signal(self, d):
        print(d)
        crsDest = QgsCoordinateReferenceSystem(
            f"PROJ:+proj=ortho +lat_0=0 +lon_0={d} +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs")

        self.mapCanvas.setDestinationCrs(crsDest)
        self.mapCanvas.refresh()


if __name__ == '__main__':
    qgsAPP = QgsApplication([], True)
    QgsApplication.setPrefixPath("qgis", True)

    qgsAPP.initQgis()

    myApp = MyApp()
    myApp.show()

    qgsAPP.exec_()
    qgsAPP.exitQgis()
