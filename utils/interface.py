# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/5/5 15:21
from PyQt5.QtCore import QSize
from qgis.gui import QgisInterface

from widgets.mainWindow import MainWindow


def initInterface(mainWindow):
    iface = Interface(mainWindow)
    return iface


class Interface(QgisInterface):
    def __init__(self, mainWindow: MainWindow):
        super(Interface, self).__init__()

        self._mainWindow = mainWindow

    def mapCanvas(self):
        return self._mainWindow.mapCanvas

    def addToolBar(self, *__args):
        toolBar = self._mainWindow.addToolBar(*__args)
        return toolBar

    def iconSize(self, dockedToolbar=False):
        return QSize(24, 24)
