# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/4/19 16:23

from qgis.core import QgsApplication

from splash import SplashScreen
from widgets.main import MainWindow

# 创建对QgsApplication的引用，第二个参数设置为False将禁用GUI
qgs = QgsApplication([], True)

# 启动画面
splash = SplashScreen()
splash.show()
# 提供qgis安装位置的路径(windows默认：C:\Program Files\QGIS 3.4\apps\qgis-ltr)
qgs.setPrefixPath("qgis", True)
# 初始化
qgs.initQgis()
# 主窗口
mainWindow = MainWindow()
splash.finish(mainWindow)
mainWindow.show()
# 脚本完成后，调用exitQgis()从内存中删除提供者和图层注册
qgs.exec_()
qgs.exitQgis()
