# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/4/21 21:44
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtWidgets import QSplashScreen, QApplication


class SplashScreen(QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()

        # 静态图片
        # pixmap = QPixmap(r'000.jpg')
        # self.setPixmap(pixmap)
        self.resize(300, 200)
        self.move(int((QApplication.desktop().width() - self.width()) / 2),
                  int((QApplication.desktop().height() - self.height()) / 2))

    def mousePressEvent(self, event):
        pass

    def paintEvent(self, event):
        # super(SplashScreen, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        font = QFont('Microsoft Yahei', 50)
        painter.setFont(font)
        painter.setPen(QColor(53, 146, 196))
        painter.drawText(30, 125, "PYQGIS")
