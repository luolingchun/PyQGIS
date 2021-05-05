# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/10/20 15:01
from qgis.PyQt.QtWidgets import QDialog, QHBoxLayout
from qgis.core import QgsVectorLayerCache
from qgis.gui import QgsAttributeTableView, QgsAttributeTableModel, QgsAttributeTableFilterModel


class AttributeDialog(QDialog):
    def __init__(self, mapCanvas, parent=None):
        super().__init__(parent)
        self.mapCanvas = mapCanvas

        self.resize(600, 400)

        self.tableView = QgsAttributeTableView(self)

        self.hl = QHBoxLayout(self)
        self.hl.addWidget(self.tableView)

    def openAttributeDialog(self, layer):
        self.layerCache = QgsVectorLayerCache(layer, layer.featureCount())
        self.tableModel = QgsAttributeTableModel(self.layerCache)
        self.tableModel.loadLayer()

        self.tableFilterModel = QgsAttributeTableFilterModel(self.mapCanvas, self.tableModel, parent=self.tableModel)
        self.tableFilterModel.setFilterMode(QgsAttributeTableFilterModel.ShowAll)
        self.tableView.setModel(self.tableFilterModel)
