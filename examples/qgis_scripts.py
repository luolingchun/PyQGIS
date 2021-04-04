# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/4/3 10:52
import os
import sys

from qgis.core import QgsApplication, QgsProcessingAlgorithm

# 提供qgis安装位置的路径(windows默认：C:\Program Files\QGIS 3.x\apps\qgis-ltr)
QgsApplication.setPrefixPath("/path/to/qgis/installation", True)
# 创建对QgsApplication的引用，第二个参数设置为False将禁用GUI
qgs = QgsApplication([], False)
# 加载提供者
qgs.initQgis()
prefix = QgsApplication.prefixPath()
print(prefix)

# 在这里编写代码，加载一些图层，使用处理算法等
sys.path.append(os.path.join(prefix, "python", "plugins"))
from plugins.processing.core.Processing import Processing
from plugins import processing

Processing.initialize()

for alg in QgsApplication.processingRegistry().algorithms():
    alg: QgsProcessingAlgorithm
    print(alg.group(), alg.provider().name(), alg.name())

result = processing.run('gdal:gdalinfo',
                        {
                            'EXTRA': '',
                            'INPUT': '../data/test.tif',
                            'MIN_MAX': False,
                            'NOGCP': False,
                            'NO_METADATA': False,
                            # 'OUTPUT': 'TEMPORARY_OUTPUT',
                            'OUTPUT': '../data/test.html',
                            'STATS': False
                        }
                        )
print(result)
# 脚本完成后，调用exitQgis（）从内存中删除提供者和图层注册
qgs.exitQgis()
