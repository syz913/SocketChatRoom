import Ui_Form.images_rc
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_register(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(340, 245)

        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap(":/image/sky.jpg")))  
        Form.setPalette(palette)
        Form.setAutoFillBackground(True) 

        Form.setStyleSheet("color:white")

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(130, 60, 150, 100))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.NamelineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.NamelineEdit.setObjectName("NamelineEdit")
        self.NamelineEdit.setStyleSheet(
            "color:black"
        )
        self.verticalLayout_3.addWidget(self.NamelineEdit)
        self.PasslineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.PasslineEdit.setObjectName("PasslineEdit")
        self.PasslineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasslineEdit.setStyleSheet(
            "color:black"
        )
        self.verticalLayout_3.addWidget(self.PasslineEdit)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(100, 30, 141, 21))
        self.label.setObjectName("label")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, -2, 70, 147))
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
        self.Passlabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Passlabel.setObjectName("Passlabel")
        self.verticalLayout_4.addWidget(self.Passlabel)
        self.RegisterButton = QtWidgets.QPushButton(Form)
        self.RegisterButton.setGeometry(QtCore.QRect(150, 180, 80, 28))
        self.RegisterButton.setObjectName("RegisterButton")
        self.RegisterButton.setStyleSheet(
            "QPushButton{background-color:rgb(255,255,255);border: 0px solid black;border-radius:8px;color:black}"
            "QPushButton:hover{background-color: rgb(255, 0, 0);border:none;color:rgb(255, 255, 255);}"
        )
        op2 = QtWidgets.QGraphicsOpacityEffect()
        op2.setOpacity(0.8)
        self.RegisterButton.setGraphicsEffect(op2)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Register"))
        self.Namelabel.setText(_translate("Form", "UserName"))
        self.Passlabel.setText(_translate("Form", "PassWord"))
        self.RegisterButton.setText(_translate("Form", "Register"))
        self.RegisterButton.setToolTip(_translate("From", "<font color='black'>ENTER</font>"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_register()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())