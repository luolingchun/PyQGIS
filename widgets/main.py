# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/4/21 21:40

from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QHBoxLayout, QVBoxLayout
from qgis.core import QgsVectorLayer, QgsProject, QgsLayerTreeModel
from qgis.gui import QgsMapCanvas, QgsMapToolZoom, QgsMapToolPan, QgsMapToolIdentifyFeature, QgsLayerTreeView, \
    QgsLayerTreeMapCanvasBridge

from ui.main_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # 调整窗口大小
        self.resize(800, 600)
        # 初始化图层树
        vl = QVBoxLayout(self.dockWidgetContents)
        self.layerTreeView = QgsLayerTreeView(self)
        vl.addWidget(self.layerTreeView)
        # 初始化地图画布
        self.mapCanvas = QgsMapCanvas(self)
        hl = QHBoxLayout(self.frame)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.addWidget(self.mapCanvas)

        # 建立桥梁
        model = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot(), self)
        model.setFlag(QgsLayerTreeModel.AllowNodeRename)
        model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        model.setFlag(QgsLayerTreeModel.ShowLegendAsTree)
        model.setAutoCollapseLegendNodes(10)
        self.layerTreeView.setModel(model)
        self.layerTreeBridge = QgsLayerTreeMapCanvasBridge(QgsProject.instance().layerTreeRoot(), self.mapCanvas)

        self.mapCanvas.xyCoordinates.connect(self.showLngLat)

        # self.actionPan.triggered.connect(self.actionPanTriggered)
        # self.actionIdentify.triggered.connect(self.actionIdentifyTriggered)

    def addTools(self):
        self.actionZoomIn = QAction("放大", self)
        self.actionZoomOut = QAction("缩小", self)
        self.actionPan = QAction("抓手", self)
        self.actionIdentify = QAction("识别", self)
        # self.toolBar.addAction(self.actionZoomIn)
        # self.toolBar.addAction(self.actionZoomOut)
        self.toolBar.addAction(self.actionPan)
        self.toolBar.addAction(self.actionIdentify)

    def addMap(self):
        data_file, ext = QFileDialog.getOpenFileName(self, '打开', '', '所有文件(*)')
        if data_file:
            if data_file.endswith(".shp") or data_file.endswith(".geojson"):
                self.layer = QgsVectorLayer(data_file, "shp", "ogr")
                QgsProject.instance().addMapLayer(self.layer)
                ids = QgsProject.instance().mapLayers()
                layers = [self.layer] + [QgsProject.instance().mapLayer(i) for i in ids]
                self.mapCanvas.setLayers(layers)
                self.mapCanvas.setExtent(self.layer.extent())
                self.mapCanvas.refresh()
            elif data_file.endswith(".csv"):
                uri = f"data_file?delimiter=,&xField=X&yField=Y"
                vlayer = QgsVectorLayer(uri, "news", "delimitedtext")
                print(vlayer.isValid())
                QgsProject.instance().addMapLayer(vlayer)
                self.mapCanvas.setLayers([vlayer, self.layer])
                # self.mapCanvas.setExtent(vlayer.extent())
                self.mapCanvas.refresh()
            else:
                print('error')

    def showLngLat(self, point):
        x = point.x()
        y = point.y()
        self.statusbar.showMessage(f'经度:{x}, 纬度:{y}')

    def actionZoomInTriggered(self):
        self.mapTool = QgsMapToolZoom(self.mapCanvas, False)
        self.mapCanvas.setMapTool(self.mapTool)

    def actionZoomOutTriggered(self):
        self.mapTool = QgsMapToolZoom(self.mapCanvas, True)
        self.mapCanvas.setMapTool(self.mapTool)

    def actionPanTriggered(self):
        self.mapTool = QgsMapToolPan(self.mapCanvas)
        self.mapCanvas.setMapTool(self.mapTool)

    def actionIdentifyTriggered(self):
        # self.mapTool = QgsMapToolIdentify(self.mapCanvas)
        # self.mapCanvas.setMapTool(self.mapTool)
        # 设置识别工具
        self.identifyTool = QgsMapToolIdentifyFeature(self.mapCanvas)
        # 发送识别的要素
        self.identifyTool.featureIdentified.connect(self.print_features)
        self.mapCanvas.setMapTool(self.identifyTool)

        # 设置需要识别的图层
        self.identifyTool.setLayer(self.layer)

    def print_features(self, feature):
        print(feature.attributes())
        print(feature.fields())
        print(feature.geometry())

        attributes = feature.attributes()
        title = attributes[0]
        time = attributes[1]
        media = attributes[2]
        link = attributes[3]
        content = attributes[4]

        title = title if title else ''
        time = time if time else ''
        media = media if media else ''
        link = link if link else ''
        content = content if content else ''

        self.newsDialog = MainWindow(self)
        self.newsDialog.lineEditTitle.setText(title)
        self.newsDialog.lineEditTime.setText(time)
        self.newsDialog.lineEditMedia.setText(media)
        self.newsDialog.lineEditLink.setText(link)
        self.newsDialog.textEditContent.setText(content)
        self.newsDialog.exec_()
