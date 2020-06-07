# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/4/21 21:40
import os

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QHBoxLayout, QVBoxLayout, QMessageBox, QDialog
from qgis.core import QgsVectorLayer, QgsProject, QgsLayerTreeModel, QgsDataSourceUri, QgsRasterLayer, \
    QgsCoordinateReferenceSystem, QgsCoordinateTransformContext, QgsPointXY
from qgis.gui import QgsMapCanvas, QgsMapToolZoom, QgsMapToolPan, QgsMapToolIdentifyFeature, QgsLayerTreeView, \
    QgsLayerTreeMapCanvasBridge, QgsVertexMarker

from ui.main_ui import Ui_MainWindow
from widgets.PostGIS import PostGISDialog
from widgets.custom_maptool import RectangleMapTool, PolygonMapTool, PointMapTool, LineMapTool

PROJECT = QgsProject.instance()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.first_flag = True
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
        model = QgsLayerTreeModel(PROJECT.layerTreeRoot(), self)
        model.setFlag(QgsLayerTreeModel.AllowNodeRename)
        model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        model.setFlag(QgsLayerTreeModel.ShowLegendAsTree)
        model.setAutoCollapseLegendNodes(10)
        self.layerTreeView.setModel(model)
        self.layerTreeBridge = QgsLayerTreeMapCanvasBridge(PROJECT.layerTreeRoot(), self.mapCanvas)
        # 显示经纬度
        self.mapCanvas.xyCoordinates.connect(self.showLngLat)

        # 打开工程
        self.actionOpen.triggered.connect(self.actionOpenTriggered)
        # 退出程序
        self.actionQuit.triggered.connect(self.close)

        # 地图工具
        # TODO:放大、缩小没有图标
        self.actionPanTriggered()
        self.actionPan.triggered.connect(self.actionPanTriggered)
        self.actionZoomin.triggered.connect(self.actionZoomInTriggered)
        self.actionZoomout.triggered.connect(self.actionZoomOutTriggered)
        self.actionIdentity.triggered.connect(self.actionIdentifyTriggered)

        # 图层
        self.actionShapefile.triggered.connect(self.actionShapefileTriggered)
        self.actionCsv.triggered.connect(self.actionCsvTriggered)
        self.actionPostGIS.triggered.connect(self.actionPostGISTriggered)
        self.actionWFS.triggered.connect(self.actionWFSTriggered)

        self.actionGeotiff.triggered.connect(self.actionGeotiffTriggered)
        self.actionXYZ.triggered.connect(self.actionXYZTriggered)

        # 绘图工具
        self.actionPoint.triggered.connect(self.actionPointTriggered)
        self.actionLine.triggered.connect(self.actionLineTriggered)
        self.actionRectangle.triggered.connect(self.actionRectangleTriggered)
        self.actionPolygon.triggered.connect(self.actionPolygonTriggered)

        # 关于Qt
        self.actionAboutQt.triggered.connect(lambda: QMessageBox.aboutQt(self, '关于Qt'))
        self.actionAbout.triggered.connect(lambda: QMessageBox.about(self, '关于', 'PyQGIS二次开发'))

        # self.actionPan.triggered.connect(self.actionPanTriggered)
        # self.actionIdentify.triggered.connect(self.actionIdentifyTriggered)

    def actionOpenTriggered(self):
        """打开工程"""
        data_file, ext = QFileDialog.getOpenFileName(self, '打开', '', '工程文件(*.qgs , *.qgz)')
        if data_file:
            PROJECT.read(data_file)

    def actionPanTriggered(self):
        self.mapTool = QgsMapToolPan(self.mapCanvas)
        self.mapCanvas.setMapTool(self.mapTool)

    def actionZoomInTriggered(self):
        self.mapTool = QgsMapToolZoom(self.mapCanvas, False)
        self.mapCanvas.setMapTool(self.mapTool)

    def actionZoomOutTriggered(self):
        self.mapTool = QgsMapToolZoom(self.mapCanvas, True)
        self.mapCanvas.setMapTool(self.mapTool)

    def actionIdentifyTriggered(self):
        # 设置识别工具
        self.identifyTool = QgsMapToolIdentifyFeature(self.mapCanvas)
        self.identifyTool.featureIdentified.connect(self.showFeatures)
        self.mapCanvas.setMapTool(self.identifyTool)

        # 设置需要识别的图层
        layers = self.mapCanvas.layers()
        if layers:
            # 识别画布中第一个图层
            self.identifyTool.setLayer(layers[0])

    def showFeatures(self, feature):
        print(type(feature))

        QMessageBox.information(self, '信息', ''.join(feature.attributes()))

    def actionShapefileTriggered(self):
        """打开shp"""
        data_file, ext = QFileDialog.getOpenFileName(self, '打开', '', '*.shp')
        if data_file:
            layer = QgsVectorLayer(data_file, "shp", "ogr")
            self.addLayer(layer)

    def actionCsvTriggered(self):
        """加载csv数据，TODO:存在问题,图层无效"""
        data_file, ext = QFileDialog.getOpenFileName(self, '打开', '', '*.csv')
        if data_file:
            uri = f"file://{data_file}?delimiter=,&xField=x&yField=y"
            print(uri)
            layer = QgsVectorLayer(uri, "point", "delimitedtext")
            self.addLayer(layer)

    def actionPostGISTriggered(self):
        """加载postgis图层"""
        dialog = PostGISDialog(self)
        if dialog.exec_():
            uri = QgsDataSourceUri()
            uri.setConnection(
                dialog.lineEditHost.text(),
                dialog.lineEditPort.text(),
                dialog.lineEditDatabase.text(),
                dialog.lineEditUsername.text(),
                dialog.lineEditPassword.text())
            # lineEditGeometryColumn：根据实际情况，可能为：wkb_geometry、geometry、the_geom...
            uri.setDataSource("public",
                              dialog.lineEditLayer.text(),
                              dialog.lineEditGeometryColumn.text())

            layer = QgsVectorLayer(uri.uri(False), dialog.lineEditLayer.text(), "postgres")
            self.addLayer(layer)

    def actionWFSTriggered(self):
        """加载天地图WFS图层"""
        uri = 'http://gisserver.tianditu.gov.cn/TDTService/wfs?' \
              'srsname=EPSG:4326&typename=TDTService:RESA&version=auto&request=GetFeature&service=WFS'
        layer = QgsVectorLayer(uri, "RESA", "WFS")
        self.addLayer(layer)

    def actionGeotiffTriggered(self):
        """加载geotiff"""
        data_file, ext = QFileDialog.getOpenFileName(self, '打开', '', '*.tif')
        if data_file:
            layer = QgsRasterLayer(data_file, os.path.basename(data_file))
            self.addLayer(layer)

    def actionXYZTriggered(self):
        uri = 'type=xyz&' \
              'url=https://www.google.cn/maps/vt?lyrs=s@804%26gl=cn%26x={x}%26y={y}%26z={z}&' \
              'zmax=19&' \
              'zmin=0&' \
              'crs=EPSG3857'
        layer = QgsRasterLayer(uri, 'google', 'wms')
        self.addLayer(layer)

    def addLayer(self, layer):
        if layer.isValid():
            if self.first_flag:
                self.mapCanvas.setDestinationCrs(layer.crs())
                self.mapCanvas.setExtent(layer.extent())
                self.first_flag = False
            PROJECT.addMapLayer(layer)
            layers = [layer] + [PROJECT.mapLayer(i) for i in PROJECT.mapLayers()]
            self.mapCanvas.setLayers(layers)
            self.mapCanvas.refresh()
        else:
            print('图层无效.')

    def actionPointTriggered(self):
        self.pointTool = PointMapTool(self.mapCanvas)
        self.mapCanvas.setMapTool(self.pointTool)

    def actionLineTriggered(self):
        self.lineTool = LineMapTool(self.mapCanvas)
        self.mapCanvas.setMapTool(self.lineTool)

    def actionRectangleTriggered(self):
        self.rectangleTool = RectangleMapTool(self.mapCanvas)
        self.mapCanvas.setMapTool(self.rectangleTool)

    def actionPolygonTriggered(self):
        self.polygonTool = PolygonMapTool(self.mapCanvas)
        self.mapCanvas.setMapTool(self.polygonTool)

    def showLngLat(self, point):
        x = point.x()
        y = point.y()
        self.statusbar.showMessage(f'经度:{x}, 纬度:{y}')
