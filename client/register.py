import socket
import sys
import threading
import time
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_Form.Ui_register import Ui_register
import DataBase
import secret

class RegisterWidget(QtWidgets.QWidget, Ui_register):
    def __init__(self, parent=None):
        super(RegisterWidget, self).__init__(parent)
        # UI
        self.setupUi(self)
        self.RegisterButton.clicked.connect(self.register)

    def register(self):
         # init db
        self.conn_db = sqlite3.connect('socketdb.db')
        cursor = self.conn_db.execute("select username from users")
        users.clear()
        for user in cursor:
            users.append(user[0])
        username = self.NamelineEdit.text()
        password = self.PasslineEdit.text()
        c = self.conn_db.cursor()
        if username == "" or password == "":
            QtWidgets.QMessageBox.warning(self, "Warning", "<font color='black'>Name or password can't be NULL!</font>",
                            QtWidgets.QMessageBox.NoButton)
            return
        if username in users:
            QtWidgets.QMessageBox.warning(self, "Warning", "<font color='black'>" + username + " is already exist!</font>",
                            QtWidgets.QMessageBox.NoButton)
            return
        else:
            keys = secret.get_key()
            public_key = keys["public_key"]
            private_key = keys["private_key"]
            signature = secret.rsa_sinature_encode(password, private_key)
            c.execute("insert into users (username, public_key, signature) values (?, ?, ?)",
                (username, public_key, signature))
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

users = []
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Client = RegisterWidget()
    Client.show()
    sys.exit(app.exec_())
