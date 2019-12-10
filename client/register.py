import socket
import sys
import threading
import time
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_Form.Ui_register import Ui_register
import DataBase

class RegisterWidget(QtWidgets.QWidget, Ui_register):
    def __init__(self, parent=None):
        super(RegisterWidget, self).__init__(parent)
        # UI
        self.setupUi(self)
        self.RegisterButton.clicked.connect(self.register)

    def register(self):
         # init db
        self.conn_db = sqlite3.connect('socketdb.db')
        cursor = self.conn_db.execute("select username, password from users")
        users.clear()
        for user in cursor:
            users[user[0]] = user[1]
        username = self.NamelineEdit.text()
        password = self.PasslineEdit.text()
        c = self.conn_db.cursor()
        if username == "" or password == "":
            QtWidgets.QMessageBox.warning(self, "Warning", "<font color='black'>Name or password can't be NULL!</font>",
                            QtWidgets.QMessageBox.NoButton)
            return
        if username in users.keys():
            QtWidgets.QMessageBox.warning(self, "Warning", "<font color='black'>" + username + " is already exist!</font>",
                            QtWidgets.QMessageBox.NoButton)
            return
        else:
            c.execute("insert into users values ('"+ username + "','" + password + "')")
            self.conn_db.commit()
        msg = QtWidgets.QMessageBox()
        reply = msg.warning(self, "Warning", "<font color='black'>Register successfully!</font>",
                            QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            self.conn_db.close()
            self.close()
        
    # keyboard events
    def keyPressEvent(self, event):
        # event.key（）display the code
        # print("press: " + str(event.key()))
        if (event.key() == QtCore.Qt.Key_Escape):
            self.close()
        if (event.key() + 1 == QtCore.Qt.Key_Enter):
            self.register()

users = {}
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Client = RegisterWidget()
    Client.show()
    sys.exit(app.exec_())
