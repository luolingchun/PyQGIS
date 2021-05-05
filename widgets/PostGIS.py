# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/6/7 12:33
from qgis.PyQt.QtWidgets import QDialog

from ui.PostGIS_ui import Ui_Dialog


class PostGISDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(PostGISDialog, self).__init__(parent)

        self.setupUi(self)

        self.pushButtonOk.clicked.connect(self.accept)
