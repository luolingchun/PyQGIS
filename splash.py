# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/4/21 21:44
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtWidgets import QSplashScreen, QApplication, QDesktopWidget


class SplashScreen(QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()

        # 静态图片
        # pixmap = QPixmap(r'000.jpg')
        # self.setPixmap(pixmap)
        self.resize(300, 200)
        self.move_center()

    def mousePressEvent(self, event):
        pass

    def move_center(self):
        # 获取屏幕分辨率
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def paintEvent(self, event):
        # super(SplashScreen, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        font = QFont('Microsoft Yahei', 50)
        painter.setFont(font)
        painter.setPen(QColor(53, 146, 196))
        painter.drawText(30, 125, "PYQGIS")
