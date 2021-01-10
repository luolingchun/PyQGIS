# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/4/21 21:44
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSplashScreen


class NewSplashScreen(QSplashScreen):
    def __init__(self):
        super(NewSplashScreen, self).__init__()
        self.setPixmap(QPixmap('./images/splash.png'))

    def mousePressEvent(self, event):
        pass
