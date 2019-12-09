import socket
import sys
import threading
import time
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_Form.Ui_login import Ui_login
import chat
import register
import DataBase

class ClientWidget(QtWidgets.QWidget, Ui_login):
    def __init__(self, parent=None):
        super(ClientWidget, self).__init__(parent)
        # init db
        # DataBase.run()
        # connection
        self.conn = socket.socket()
        self.connected = False
        self.username = ''
        # UI
        self.setupUi(self)
        # self.IPlineEdit.setText("127.0.0.1")
        # self.IPlineEdit.setEnabled(False)
        # self.PortlineEdit.setText("30153")
        # self.PortlineEdit.setEnabled(False)
        # self.LoginButton.setShortcut(QtCore.Qt.Key_Return)
        self.LoginButton.clicked.connect(self.connect_server)
        self.RegisterButton.clicked.connect(self.register)

    def connect_server(self):
        conn_db = sqlite3.connect('pydb.db')
        print ("Opened database successfully")
        cursor = conn_db.execute("select username, password from users")
        users.clear()
        for user in cursor:
            users[user[0]] = user[1]
        if self.connected:
            return
        name = self.NamelineEdit.text()
        password = self.PasslineEdit.text()
        # special case: no name
        if name == "" or password == "":
            # self.connStatus.setText("NameError: Name Can't be NULL!")
            QtWidgets.QMessageBox.warning(self, "Warning", "<font color='black'>Name or password can't be NULL!</font>", QtWidgets.QMessageBox.NoButton)
            return
        self.username = name            
        # IP = self.IPlineEdit.text()
        # if IP == "":
        #     IP = "127.0.0.1"
        # port = self.PortlineEdit.text()
        # if port == "" or not port.isnumeric():
        #     self.PortlineEdit.setText("30153")
        #     # self.connStatus.setText("PortError: format invalid")
        #     QtWidgets.QMessageBox.warning(self, "Warning", "PortError: format invalid", QtWidgets.QMessageBox.Ok)
        #     return
        # else:
        #     port = int(port)
        if name in users.keys():
            if users[name] == password:
                IP = "127.0.0.1"
                port = 30153
                if ChatWidget.connect_server(name, IP, port) == True:
                    self.connected = True
                    # self.connStatus.setText("You are Connected")
                    self.NamelineEdit.setReadOnly(True)
                else:
                    QtWidgets.QMessageBox.warning(self, "Warning", "<font color='black'>Connection Refused!</font>",
                            QtWidgets.QMessageBox.NoButton)
                    # self.connStatus.setText("Connection Refused")
                    self.conn = socket.socket()
                    return
                self.close()
                ChatWidget.show()
            else:
                QtWidgets.QMessageBox.warning(self, "Warning", "<font color='black'>password is wrong!</font>",
                            QtWidgets.QMessageBox.NoButton)
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "<font color='black'>" + name + " isn't exist!</font>",
                            QtWidgets.QMessageBox.NoButton)
    
    def register(self):
        RegisterWidget.show()
        
    # keyboard events
    def keyPressEvent(self, event):
        # event.key（）display the code
        # print("press: " + str(event.key()))
        if (event.key() == QtCore.Qt.Key_Escape):
            self.close()
        if (event.key() + 1 == QtCore.Qt.Key_Enter):
            self.connect_server()
        if (event.key() == QtCore.Qt.Key_R):
            if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
                self.register()
            else:
                print("enter")

users = {}
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Client = ClientWidget()
    ChatWidget = chat.ChatWidget() 
    RegisterWidget = register.RegisterWidget()
    Client.show()
    sys.exit(app.exec_())
