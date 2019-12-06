import socket
import sys
import threading
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_Form.Ui_login import Ui_login
import chat

class ClientWidget(QtWidgets.QWidget, Ui_login):
    def __init__(self, parent=None):
        super(ClientWidget, self).__init__(parent)
        # connection
        self.conn = socket.socket()
        self.connected = False
        self.username = ''
        # UI
        self.setupUi(self)
        self.IPlineEdit.setText("127.0.0.1")
        self.IPlineEdit.setEnabled(False)
        self.PortlineEdit.setText("30153")
        self.PortlineEdit.setEnabled(False)
        # self.LoginButton.setShortcut(QtCore.Qt.Key_Return)
        self.LoginButton.clicked.connect(self.connect_server)

    def connect_server(self):
        if self.connected:
            return
        name = self.NamelineEdit.text()
        # special case: no name
        if name == "":
            # self.connStatus.setText("NameError: Name Can't be NULL!")
            QtWidgets.QMessageBox.warning(self, "Warning", "NameError: Name Can't be NULL!", QtWidgets.QMessageBox.Ok)
            return
        self.username = name
        IP = self.IPlineEdit.text()
        if IP == "":
            IP = "127.0.0.1"
        port = self.PortlineEdit.text()
        if port == "" or not port.isnumeric():
            self.PortlineEdit.setText("30153")
            # self.connStatus.setText("PortError: format invalid")
            QtWidgets.QMessageBox.warning(self, "Warning", "PortError: format invalid", QtWidgets.QMessageBox.Ok)
            return
        else:
            port = int(port)
        if ChatWidget.connect_server(name, IP, port) == True:
            self.connected = True
            # self.connStatus.setText("You are Connected")
            self.NamelineEdit.setReadOnly(True)
        else:
            self.connStatus.setText("Connection Refused")
            self.conn = socket.socket()
            return
        self.close()
        ChatWidget.show()
        
    # keyboard events
    def keyPressEvent(self, event):
        # event.key（）display the code
        # print("press: " + str(event.key()))
        if (event.key() == QtCore.Qt.Key_Escape):
            self.close()
        if (event.key() + 1 == QtCore.Qt.Key_Enter):
            self.connect_server()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Client = ClientWidget()
    ChatWidget = chat.ChatWidget()  # 生成聊天界面的实例
    Client.show()
    sys.exit(app.exec_())
