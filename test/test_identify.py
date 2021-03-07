# -*- coding: utf-8 -*-
# @Time    : 2019/12/12 13:26
# @Author  : llc
# @File    : main_ui.py
import os

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout
from qgis.gui import QgsLayerTreeMapCanvasBridge, QgsLayerTreeView, QgsMapCanvas, QgsMapToolIdentifyFeature,QgisInterface
from qgis.core import QgsVectorLayer, QgsProject, QgsLayerTreeModel, QgsApplication, QgsFeature, QgsDataSourceUri, \
    QgsVectorDataProvider
from qgis.utils import iface

iface

from main_ui import Ui_MainWindow
QgsVectorDataProvider

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)

        self.layers = []

        # ---------初始化图层和画布----------
        self.vl = QVBoxLayout(self.dockWidgetContents)
        self.layer_tree_view = QgsLayerTreeView(self)
        self.vl.addWidget(self.layer_tree_view)
        self.hl = QHBoxLayout(self.frame)
        self.mapCanvas = QgsMapCanvas(self.frame)
        self.hl.addWidget(self.mapCanvas)
        # ---------初始化图层和画布----------

        self.action_open.triggered.connect(self.action_open_triggered)

        # 建立桥梁
        self.model = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot(), self)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeRename)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.model.setFlag(QgsLayerTreeModel.ShowLegendAsTree)
        self.model.setAutoCollapseLegendNodes(10)
        self.layer_tree_view.setModel(self.model)
        self.layer_tree_bridge = QgsLayerTreeMapCanvasBridge(QgsProject.instance().layerTreeRoot(), self.mapCanvas)

        # 设置识别工具
        self.identifyTool = QgsMapToolIdentifyFeature(self.mapCanvas)
        # 发送识别的要素
        self.identifyTool.featureIdentified.connect(self.print_features)
        self.mapCanvas.setMapTool(self.identifyTool)

    def action_open_triggered(self):
        data_file, ext = QFileDialog.getOpenFileName(self, '打开', '', '所有文件(*)')
        if data_file:
            if data_file.endswith('.shp'):
                basename = os.path.splitext(os.path.basename(data_file))[0]
                layer = QgsVectorLayer(data_file, basename, "ogr")
                QgsProject.instance().addMapLayer(layer)
                self.layers.append(layer)
                self.mapCanvas.setExtent(layer.extent())
                self.mapCanvas.setLayers(self.layers)
                self.mapCanvas.refresh()
                self.layer_tree_view.setCurrentLayer(layer)

                # 设置需要识别的图层
                self.identifyTool.setLayer(layer)

            elif data_file.endswith('.qgz') or data_file.endswith('.qgs'):
                QgsProject.instance().read(data_file)
            else:
                print('error')

    def print_features(self, feature):
        print(feature.attributes())
        print(feature.fields())
        print(feature.geometry())


if __name__ == '__main__':
    # 应用入口，使用GUI
    qgs = QgsApplication([], True)
    # 设置，qgis安装路径，这里写相对路径，如果是源码运行，这行可不写
    qgs.setPrefixPath('qgis', True)
    # 初始化
    qgs.initQgis()

    window = Window()
    window.show()

    exit_code = qgs.exec_()
    # 退出
    qgs.exitQgis()
