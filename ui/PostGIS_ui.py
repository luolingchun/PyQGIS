# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PostGIS.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(442, 448)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEditDatabase = QtWidgets.QLineEdit(Dialog)
        self.lineEditDatabase.setObjectName("lineEditDatabase")
        self.gridLayout.addWidget(self.lineEditDatabase, 2, 2, 1, 1)
        self.lineEditLayer = QtWidgets.QLineEdit(Dialog)
        self.lineEditLayer.setObjectName("lineEditLayer")
        self.gridLayout.addWidget(self.lineEditLayer, 5, 2, 1, 1)
        self.lineEditHost = QtWidgets.QLineEdit(Dialog)
        self.lineEditHost.setObjectName("lineEditHost")
        self.gridLayout.addWidget(self.lineEditHost, 0, 2, 1, 1)
        self.lineEditPort = QtWidgets.QLineEdit(Dialog)
        self.lineEditPort.setObjectName("lineEditPort")
        self.gridLayout.addWidget(self.lineEditPort, 1, 2, 1, 1)
        self.lineEditPassword = QtWidgets.QLineEdit(Dialog)
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.gridLayout.addWidget(self.lineEditPassword, 4, 2, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.lineEditGeometryColumn = QtWidgets.QLineEdit(Dialog)
        self.lineEditGeometryColumn.setObjectName("lineEditGeometryColumn")
        self.gridLayout.addWidget(self.lineEditGeometryColumn, 6, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.lineEditUsername = QtWidgets.QLineEdit(Dialog)
        self.lineEditUsername.setObjectName("lineEditUsername")
        self.gridLayout.addWidget(self.lineEditUsername, 3, 2, 1, 1)
        self.pushButtonOk = QtWidgets.QPushButton(Dialog)
        self.pushButtonOk.setObjectName("pushButtonOk")
        self.gridLayout.addWidget(self.pushButtonOk, 7, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lineEditDatabase.setText(_translate("Dialog", "test2020"))
        self.lineEditLayer.setText(_translate("Dialog", "lakes"))
        self.lineEditHost.setText(_translate("Dialog", "localhost"))
        self.lineEditPort.setText(_translate("Dialog", "5432"))
        self.lineEditPassword.setText(_translate("Dialog", "123456"))
        self.label.setText(_translate("Dialog", "host:"))
        self.label_4.setText(_translate("Dialog", "password:"))
        self.label_3.setText(_translate("Dialog", "username:"))
        self.label_7.setText(_translate("Dialog", "geometry column："))
        self.label_2.setText(_translate("Dialog", "port:"))
        self.label_5.setText(_translate("Dialog", "database:"))
        self.lineEditGeometryColumn.setText(_translate("Dialog", "wkb_geometry"))
        self.label_6.setText(_translate("Dialog", "layer:"))
        self.lineEditUsername.setText(_translate("Dialog", "postgres"))
        self.pushButtonOk.setText(_translate("Dialog", "ok"))

