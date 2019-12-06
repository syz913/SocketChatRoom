# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Windows\Desktop\计算机网络\Lab\final-pj\Socket-Project\client\Ui_Form\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_login(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(340, 245)

        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap(":/image/sky.jpg")))  
        Form.setPalette(palette)
        Form.setAutoFillBackground(True) 

        Form.setStyleSheet("color:white")

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(110, 60, 161, 121))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.PortlineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.PortlineEdit.setObjectName("PortlineEdit")
        self.PortlineEdit.setStyleSheet(
            "color:black"
        )
        self.verticalLayout_3.addWidget(self.PortlineEdit)
        self.IPlineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.IPlineEdit.setObjectName("IPlineEdit")
        self.IPlineEdit.setStyleSheet(
            "color:black"
        )
        self.verticalLayout_3.addWidget(self.IPlineEdit)
        self.NamelineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.NamelineEdit.setObjectName("NamelineEdit")
        self.NamelineEdit.setStyleSheet(
            "color:black"
        )
        self.verticalLayout_3.addWidget(self.NamelineEdit)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(110, 20, 141, 21))
        self.label.setObjectName("label")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, 60, 50, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Portlabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Portlabel.setObjectName("Portlabel")
        self.verticalLayout_4.addWidget(self.Portlabel)
        self.IPlabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.IPlabel.setObjectName("IPlabel")
        self.verticalLayout_4.addWidget(self.IPlabel)
        self.Namelabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Namelabel.setObjectName("Namelabel")
        self.verticalLayout_4.addWidget(self.Namelabel)
        self.LoginButton = QtWidgets.QPushButton(Form)
        self.LoginButton.setGeometry(QtCore.QRect(120, 180, 93, 28))
        self.LoginButton.setObjectName("LoginButton")
        self.LoginButton.setStyleSheet(
            "QPushButton{background-color:rgb(255,255,255);border: 0px solid black;border-radius:8px;color:black}"
            "QPushButton:hover{background-color: rgb(255, 0, 0);border:none;color:rgb(255, 255, 255);}"
        )
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        self.LoginButton.setGraphicsEffect(op)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Login"))
        self.label.setText(_translate("Form", "Welcome To Chat!"))
        self.Portlabel.setText(_translate("Form", "Port"))
        self.IPlabel.setText(_translate("Form", "IP"))
        self.Namelabel.setText(_translate("Form", "Name"))
        self.LoginButton.setText(_translate("Form", "Login"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_login()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())