# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/4/21 21:44
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtWidgets import QSplashScreen


class NewSplashScreen(QSplashScreen):
    def __init__(self):
        super(NewSplashScreen, self).__init__()
        self.setPixmap(QPixmap('./images/splash.png'))

    def mousePressEvent(self, event):
        pass
