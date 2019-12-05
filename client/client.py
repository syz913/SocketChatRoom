import socket
import sys
import threading
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from MyQTextEdit import MyQTextEdit
# from Ui_Form.Ui_login import Ui_login
import chat

class ClientWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ClientWidget, self).__init__(parent)
        # connection
        self.conn = socket.socket()
        self.connected = False
        self.username = ''
        # # tabs
        self.layout = QtWidgets.QVBoxLayout(self)
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.resize(300, 200)
        self.tab_login = QtWidgets.QWidget()
        # self.tab_chat = QtWidgets.QWidget()
        self.tabs.addTab(self.tab_login, "Login")
        # tab: Login
        LoginGrid = QtWidgets.QGridLayout()
        self.tab_login.setLayout(LoginGrid)
        self.LoginBox = QtWidgets.QGroupBox("Login")
        self.IPLineEdit = QtWidgets.QLineEdit()
        self.IPLineEdit.setText("127.0.0.1")
        self.portLineEdit = QtWidgets.QLineEdit()
        self.portLineEdit.setText("30153")
        self.nameLineEdit = QtWidgets.QLineEdit()
        self.connIP = QtWidgets.QLabel("IP", self)
        self.connPort = QtWidgets.QLabel("Port", self)
        self.connName = QtWidgets.QLabel("Name", self)

        LoginBoxLayout = QtWidgets.QGridLayout()
        LoginBoxLayout.addWidget(self.connIP, 0, 0, 1, 1)
        LoginBoxLayout.addWidget(self.IPLineEdit, 0, 1, 1, 1)
        LoginBoxLayout.addWidget(self.connPort)
        LoginBoxLayout.addWidget(self.portLineEdit)
        LoginBoxLayout.addWidget(self.connName)
        LoginBoxLayout.addWidget(self.nameLineEdit)
        self.LoginBox.setLayout(LoginBoxLayout)

        self.connStatus = QtWidgets.QLabel("", self)
        self.connBtn = QtWidgets.QPushButton("Log in")
        self.connBtn.setShortcut(QtCore.Qt.Key_Return)
        self.connBtn.clicked.connect(self.connect_server)
        LoginGrid.addWidget(self.LoginBox, 0, 0, 2, 2)

        LoginGrid.addWidget(self.connStatus, 2, 0, 1, 1)
        LoginGrid.addWidget(self.connBtn, 3, 1, 1, 1)

        # # Initialization
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def connect_server(self):
        if self.connected:
            return
        name = self.nameLineEdit.text()
        # special case: no name
        if name == "":
            self.connStatus.setText("NameError: Name Can't be NULL!")
            return
        self.username = name
        IP = self.IPLineEdit.text()
        if IP == "":
            IP = "127.0.0.1"
        port = self.portLineEdit.text()
        if port == "" or not port.isnumeric():
            self.portLineEdit.setText("30153")
            self.connStatus.setText("PortError: format invalid")
            return
        else:
            port = int(port)
        if ChatWidget.connect_server(name, IP, port) == True:
            self.connected = True
            self.connStatus.setText("You are Connected")
            self.nameLineEdit.setReadOnly(True)
        else:
            self.connStatus.setText("Connection Refused")
            self.conn = socket.socket()
            return
        self.close()
        ChatWidget.show()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Client = ClientWidget()
    ChatWidget = chat.ChatWidget()  # 生成聊天界面的实例
    Client.show()
    sys.exit(app.exec_())
