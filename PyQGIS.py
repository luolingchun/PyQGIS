# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/4/19 16:23

from qgis.PyQt import QtCore
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsApplication

from config import setup_env
from splash import NewSplashScreen
# from utils.plugins import loadPlugins
# from utils.interface import initInterface
from widgets.mainWindow import MainWindow

# from qgis.utils import iface

# 添加插件目录
# os.environ["QGIS_PLUGINPATH"] = r"D:\workspace\QGIS\plugins"

setup_env()
# 适应高分辨率
QgsApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
# 设置窗口风格
QgsApplication.setStyle("Fusion")
# 创建对QgsApplication的引用，第二个参数设置为False将禁用GUI
qgs = QgsApplication([], True)

t = QtCore.QTranslator()  # 先新建一个 QTranslator
# 加载翻译文件
t.load(r'C:\Program Files\QGIS 3.16\apps\qgis-ltr\i18n\qgis_zh-Hans.qm')
qgs.installTranslator(t)

# 启动画面
splash = NewSplashScreen()
splash.show()
# 提供qgis安装位置的路径(windows默认：C:\Program Files\QGIS 3.4\apps\qgis-ltr)
qgs.setPrefixPath("qgis", True)
# 初始化
qgs.initQgis()

# 主窗口
mainWindow = MainWindow()
# 初始化iface
# iface = initInterface(mainWindow)
# 加载插件
# loadPlugins(iface)
# 设置图标
mainWindow.setWindowIcon(QIcon('./images/pyqgis.png'))
splash.finish(mainWindow)
mainWindow.show()
# 脚本完成后，调用exitQgis()从内存中删除提供者和图层注册
qgs.exec_()
qgs.exitQgis()
