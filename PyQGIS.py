# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/4/19 16:23
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from qgis.core import QgsApplication

from config import setup_env
from splash import NewSplashScreen
from widgets.main import MainWindow

setup_env()
# 适应高分辨率
QgsApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
# 创建对QgsApplication的引用，第二个参数设置为False将禁用GUI
qgs = QgsApplication([], True)

# 启动画面
splash = NewSplashScreen()
splash.show()
# 提供qgis安装位置的路径(windows默认：C:\Program Files\QGIS 3.4\apps\qgis-ltr)
qgs.setPrefixPath("qgis", True)
# 初始化
qgs.initQgis()
# 主窗口
mainWindow = MainWindow()
mainWindow.setWindowIcon(QIcon('./images/pyqgis.png'))
splash.finish(mainWindow)
mainWindow.show()
# 脚本完成后，调用exitQgis()从内存中删除提供者和图层注册
qgs.exec_()
qgs.exitQgis()
