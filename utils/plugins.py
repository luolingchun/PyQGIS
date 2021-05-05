# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/5/5 15:27
import os
import sys


def loadPlugins(iface):
    QGIS_PLUGINPATH = os.environ["QGIS_PLUGINPATH"]
    if not os.path.exists(QGIS_PLUGINPATH):
        print("QGIS_PLUGINPATH not exists.")
        return
    print("QGIS_PLUGINPATH:", QGIS_PLUGINPATH)
    sys.path.append(QGIS_PLUGINPATH)
    sys.path_importer_cache.clear()
    for plugin in os.listdir(QGIS_PLUGINPATH):
        if os.path.isdir(os.path.join(QGIS_PLUGINPATH, plugin)):
            # print(plugin)
            __import__(plugin)
            pluginPackage = sys.modules[plugin]
            pluginObj = pluginPackage.classFactory(iface)
            pluginObj.initGui()
