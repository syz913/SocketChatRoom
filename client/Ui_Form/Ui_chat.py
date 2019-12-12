import Ui_Form.images_rc
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_chat(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(920, 800)

        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap(":/image/sky.jpg")))  
        Widget.setPalette(palette)
        Widget.setAutoFillBackground(True) 

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Widget)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter_2 = QtWidgets.QSplitter(Widget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setOpaqueResize(False)
        self.splitter_2.setChildrenCollapsible(False)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setOpaqueResize(False)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.messageBrowser = QtWidgets.QTextBrowser(self.layoutWidget)
        self.messageBrowser.setObjectName("messageBrowser")
        self.messageBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.messageBrowser.setStyleSheet( 
            "background-color:rgb(255,255,255);border-radius:8px;padding:10px;\n"
            "background-image:url(:/image/bg1.jpg)")
        self.verticalLayout.addWidget(self.messageBrowser)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # self.sendChoice = QtWidgets.QLabel("Send to: ", self)
        # self.horizontalLayout_2.addWidget(self.sendChoice)
        self.SizeComboBox1 = QtWidgets.QComboBox(self.layoutWidget)
        self.SizeComboBox1.setObjectName("SizeComboBox1")
        self.SizeComboBox1.addItem("ALL")
        self.horizontalLayout_2.addWidget(self.SizeComboBox1)

        self.fontComboBox = QtWidgets.QFontComboBox(self.layoutWidget)
        self.fontComboBox.setObjectName("fontComboBox")
        self.horizontalLayout_2.addWidget(self.fontComboBox)

        self.SizeComboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.SizeComboBox.setObjectName("SizeComboBox")
        self.SizeComboBox.addItem("")
        self.SizeComboBox.addItem("")
        self.SizeComboBox.addItem("")
        self.SizeComboBox.addItem("")
        self.SizeComboBox.addItem("")
        self.SizeComboBox.addItem("")
        self.SizeComboBox.addItem("")
        self.SizeComboBox.addItem("")
        self.SizeComboBox.addItem("")
        self.SizeComboBox.addItem("")
        self.SizeComboBox.addItem("")
        self.SizeComboBox.addItem("")
        self.SizeComboBox.addItem("")
        self.SizeComboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.SizeComboBox)
        self.imageBtn = QtWidgets.QToolButton(self.layoutWidget)
        self.imageBtn.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/picture.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.imageBtn.setIcon(icon)
        self.imageBtn.setIconSize(QtCore.QSize(22, 22))
        self.imageBtn.setCheckable(True)
        self.imageBtn.setAutoRaise(True)
        self.imageBtn.setObjectName("imageBtn")
        self.horizontalLayout_2.addWidget(self.imageBtn)
        self.boldToolBtn = QtWidgets.QToolButton(self.layoutWidget)
        self.boldToolBtn.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/bold.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.boldToolBtn.setIcon(icon)
        self.boldToolBtn.setIconSize(QtCore.QSize(22, 22))
        self.boldToolBtn.setCheckable(True)
        self.boldToolBtn.setAutoRaise(True)
        self.boldToolBtn.setObjectName("boldToolBtn")
        self.horizontalLayout_2.addWidget(self.boldToolBtn)
        self.italicToolBtn = QtWidgets.QToolButton(self.layoutWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/image/italic.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.italicToolBtn.setIcon(icon1)
        self.italicToolBtn.setIconSize(QtCore.QSize(22, 22))
        self.italicToolBtn.setCheckable(True)
        self.italicToolBtn.setAutoRaise(True)
        self.italicToolBtn.setObjectName("italicToolBtn")
        self.horizontalLayout_2.addWidget(self.italicToolBtn)
        self.underlineToolBtn = QtWidgets.QToolButton(self.layoutWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/image/under.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.underlineToolBtn.setIcon(icon2)
        self.underlineToolBtn.setIconSize(QtCore.QSize(22, 22))
        self.underlineToolBtn.setCheckable(True)
        self.underlineToolBtn.setAutoRaise(True)
        self.underlineToolBtn.setObjectName("underlineToolBtn")
        self.horizontalLayout_2.addWidget(self.underlineToolBtn)
        self.colorToolBtn = QtWidgets.QToolButton(self.layoutWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/image/color.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.colorToolBtn.setIcon(icon3)
        self.colorToolBtn.setIconSize(QtCore.QSize(22, 22))
        self.colorToolBtn.setAutoRaise(True)
        self.colorToolBtn.setObjectName("colorToolBtn")
        self.horizontalLayout_2.addWidget(self.colorToolBtn)
        self.saveToolBtn = QtWidgets.QToolButton(self.layoutWidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/image/save.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveToolBtn.setIcon(icon4)
        self.saveToolBtn.setIconSize(QtCore.QSize(22, 22))
        self.saveToolBtn.setAutoRaise(True)
        self.saveToolBtn.setObjectName("saveToolBtn")
        self.horizontalLayout_2.addWidget(self.saveToolBtn)
        self.clearToolBtn = QtWidgets.QToolButton(self.layoutWidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/image/clear.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearToolBtn.setIcon(icon5)
        self.clearToolBtn.setIconSize(QtCore.QSize(22, 22))
        self.clearToolBtn.setAutoRaise(True)
        self.clearToolBtn.setObjectName("clearToolBtn")
        self.horizontalLayout_2.addWidget(self.clearToolBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.messageTextEdit = QtWidgets.QTextEdit(self.splitter)
        self.messageTextEdit.setObjectName("messageTextEdit")
        self.messageTextEdit.setStyleSheet(
            "background-color:rgb(255,255,255);border-radius:8px;\n"
            "margin:0px 10px 0px 10px"
        )
        self.userTableWidget = QtWidgets.QTableWidget(self.splitter_2)
        # hide the number
        self.userTableWidget.verticalHeader().setHidden(True)
        self.userTableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.userTableWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.userTableWidget.setShowGrid(True)
        self.userTableWidget.setObjectName("userTableWidget")
        self.userTableWidget.horizontalHeader().setStyleSheet(
            "font-size:30px;font-family:华文琥珀;"
        )
        self.userTableWidget.setStyleSheet(
            "background-color:rgb(255,255,255);border-radius:8px;margin-top:10px;\n"
            "background-image:url(:/image/bg2.jpg)")
        self.userTableWidget.setColumnCount(1)
        self.userTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.userTableWidget.setHorizontalHeaderItem(0, item)
        self.verticalLayout_2.addWidget(self.splitter_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            108, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        self.sendButton = QtWidgets.QPushButton(Widget)
        self.sendButton.setStyleSheet(
            "QPushButton{background-color:rgb(255,255,255);border: 0px solid black;border-radius:8px;padding:10px 30px 10px 30px}"
            "QPushButton:hover{background-color: rgb(255, 0, 0);border:none;color:rgb(255, 255, 255);}"
        )
        self.sendButton.setGraphicsEffect(op)
        self.horizontalLayout.addWidget(self.sendButton)
        spacerItem1 = QtWidgets.QSpacerItem(
            178, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.userNumLabel = QtWidgets.QLabel(Widget)
        self.userNumLabel.setObjectName("userNumLabel")
        self.horizontalLayout.addWidget(self.userNumLabel)
        spacerItem2 = QtWidgets.QSpacerItem(
            248, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.exitButton = QtWidgets.QPushButton(Widget)
        self.exitButton.setStyleSheet(
            "QPushButton{background-color:rgb(255,255,255);border: 0px solid black;border-radius:8px;padding:10px 30px 10px 30px}"
            "QPushButton:hover{background-color: rgb(255, 0, 0);border:none;color:rgb(255, 255, 255);}"
        )
        op2 = QtWidgets.QGraphicsOpacityEffect()
        op2.setOpacity(0.8)
        self.exitButton.setGraphicsEffect(op2)
        self.exitButton.setObjectName("exitButton")
        self.horizontalLayout.addWidget(self.exitButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(Widget)
        self.SizeComboBox.setCurrentIndex(0)
        self.SizeComboBox1.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Chat Room"))
        self.SizeComboBox1.setCurrentText(_translate("Widget", "All"))
        self.SizeComboBox.setCurrentText(_translate("Widget", "9"))
        self.SizeComboBox.setItemText(0, _translate("Widget", "9"))
        self.SizeComboBox.setItemText(1, _translate("Widget", "10"))
        self.SizeComboBox.setItemText(2, _translate("Widget", "11"))
        self.SizeComboBox.setItemText(3, _translate("Widget", "12"))
        self.SizeComboBox.setItemText(4, _translate("Widget", "13"))
        self.SizeComboBox.setItemText(5, _translate("Widget", "14"))
        self.SizeComboBox.setItemText(6, _translate("Widget", "15"))
        self.SizeComboBox.setItemText(7, _translate("Widget", "16"))
        self.SizeComboBox.setItemText(8, _translate("Widget", "17"))
        self.SizeComboBox.setItemText(9, _translate("Widget", "18"))
        self.SizeComboBox.setItemText(10, _translate("Widget", "19"))
        self.SizeComboBox.setItemText(11, _translate("Widget", "20"))
        self.SizeComboBox.setItemText(12, _translate("Widget", "21"))
        self.SizeComboBox.setItemText(13, _translate("Widget", "22"))
        self.imageBtn.setToolTip(_translate("Widget", "表情"))
        self.imageBtn.setText(_translate("Widget", "..."))
        self.boldToolBtn.setToolTip(_translate("Widget", "加粗"))
        self.boldToolBtn.setText(_translate("Widget", "..."))
        self.italicToolBtn.setToolTip(_translate("Widget", "倾斜"))
        self.italicToolBtn.setText(_translate("Widget", "..."))
        self.underlineToolBtn.setToolTip(_translate("Widget", "下划线"))
        self.underlineToolBtn.setText(_translate("Widget", "..."))
        self.colorToolBtn.setToolTip(_translate("Widget", "更改字体颜色"))
        self.colorToolBtn.setText(_translate("Widget", "..."))
        self.saveToolBtn.setToolTip(_translate("Widget", "保存聊天记录"))
        self.saveToolBtn.setText(_translate("Widget", "..."))
        self.clearToolBtn.setToolTip(_translate("Widget", "清空聊天记录"))
        self.clearToolBtn.setText(_translate("Widget", "..."))
        item = self.userTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Widget", "USERS"))
        self.sendButton.setText(_translate("Widget", "Send"))
        self.sendButton.setToolTip(_translate("Widget", "CTRL+ENTER"))
        self.userNumLabel.setText(_translate("Widget", "Online users: 0"))
        self.exitButton.setText(_translate("Widget", "Quit"))
        self.exitButton.setToolTip(_translate("Widget", "ESC"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_chat()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())
