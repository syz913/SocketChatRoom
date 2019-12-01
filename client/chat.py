import socket
import sys
import codecs
import threading
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt, QProcess, QDateTime, QFile, QTextStream
from PyQt5.QtGui import QFont, QColor, QTextCursor, QTextCharFormat, QTextDocumentWriter
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QFileDialog, QColorDialog, QHeaderView, QApplication, QMenu, QAction
from MyQTextEdit import MyQTextEdit
from Ui_Form.Ui_chat import Ui_chat
import client


class ChatWidget(QtWidgets.QWidget, Ui_chat):
    def __init__(self, parent=None):
        super(ChatWidget, self).__init__(parent)
        self.setupUi(self)
        self.setWindowOpacity(1)
        self.networkInit()
        self.userTableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.splitter.setStretchFactor(0, 7)
        self.splitter.setStretchFactor(1, 3)
        self.splitter_2.setStretchFactor(0, 6)
        self.splitter_2.setStretchFactor(1, 5)

    def networkInit(self):
        # send to server message type: {LOGIN}
        # message = bytes("{LOGIN}" + name, "utf-8")
        # self.conn.send(message)
        self.conn = socket.socket()
        self.username = ""
        self.connected = False
        self.sendList = "ALL"
        currentUser = ""
        self.setWindowTitle(currentUser)

    def show_message(self, newMessage, type):
        times = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        username = ""
        message = ""
        try:
            username = newMessage.split(" : ")[0]
            message = newMessage.split(" : ")[1]
            # print(message)
        except:
            pass
        if type == "Message":
            self.messageBrowser.setTextColor(Qt.blue)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 12))
            self.messageBrowser.append("[" + username + "]  " + times)
            self.messageBrowser.append(message)
        elif type == "Private":
            self.messageBrowser.setTextColor(Qt.red)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 12))
            self.messageBrowser.append("[" + username + "]  " + times)
            self.messageBrowser.append(message)
        if type == "NEW":
            self.messageBrowser.setTextColor(Qt.gray)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 10))
            self.messageBrowser.append(newMessage + "  " + times)
        if type == "LEFT":
            self.messageBrowser.setTextColor(Qt.gray)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 10))
            self.messageBrowser.append(newMessage + "  " + times)
        time.sleep(0.2)
        # self.scrollRecords.verticalScrollBar().setValue(
        #     self.scrollRecords.verticalScrollBar().maximum())

    def send_message(self):
        # Special case: friend leave as the same time with send message
        if self.sendList != self.SizeComboBox1.currentText():
            QMessageBox.warning(self, "Warning",
                                "The person has left. Private message not delivered!", QMessageBox.Ok)
            self.messageTextEdit.clear()
            return
        # line = self.messageTextEdit.toPlainText()
        message = self.getMessage()
        # Special case: Empty message
        if message == "":
            QMessageBox.warning(self, "Warning",
                                "The sending message cannot be empty", QMessageBox.Ok)
            return
        # Special case: illegal character
        if '{CLIENTS}' in message or '{MESSAGE}' in message:
            QMessageBox.warning(self, "Warning",
                                "Do not use word: '{CLIENTS}', '{MESSAGE}'", QMessageBox.Ok)
            self.messageTextEdit.clear()
            return
        # Private message: Send to me(server)
        if self.sendList != "ALL":
            message1 = bytes("{" + self.username + "}" + str(message), "utf-8")
            self.conn.sendall(message1)
            time.sleep(0.1)
        # send message to server. message type: {sendList}
        message2 = bytes("{" + self.sendList + "}" + str(message), "utf-8")
        self.conn.sendall(message2)
        self.messageTextEdit.clear()
        # self.scrollRecords.verticalScrollBar().setValue(
        #     self.scrollRecords.verticalScrollBar().maximum())

    def refresh_friendlist(self, userList):
        users = userList.split("|")
        # delete all rows
        # Attention!!!: the index of row is changed every time
        for i in range(self.userTableWidget.rowCount()):
            self.userTableWidget.removeRow(0)
        # first update the userlists
        for user in users:
            # find if user is new user
            isNew = userlists.index(user) if (user in userlists) else -1
            if isNew == -1:
                userlists.append(user)
        for user in userlists:
            print("index:" + user)
            isOnline = users.index(user) if (user in users) else -1
            if isOnline == -1:
                user = QTableWidgetItem(user+" ("+"off-line"+")")
                self.userTableWidget.insertRow(0)
                self.userTableWidget.setItem(0, 0, user)
            else:
                user = QTableWidgetItem(user+" ("+"online"+")")
                self.userTableWidget.insertRow(0)
                self.userTableWidget.setItem(0, 0, user)
        online_user_cnt = "Online users: {}".format(len(users))
        self.userNumLabel.setText(online_user_cnt)

    def refresh_sendlist(self, userList):
        users = userList.split("|")
        self.SizeComboBox1.clear()
        self.SizeComboBox1.addItem("ALL")
        for user in users:
            if user != self.username:
                self.SizeComboBox1.addItem(user)
        previous = self.sendList
        index = self.SizeComboBox1.findText(previous)
        if index != -1:
            self.SizeComboBox1.setCurrentIndex(
                index)  # updating, maintain receiver
        else:
            # friend left, set sendListBox "ALL"
            self.sendListBox.setCurrentIndex(0)

    def refresh_interface(self):
        while self.connected:
            message = self.conn.recv(1024)
            message = message.decode("utf-8")
            print(message)
            if message != "":
                # message type: CLIENTS - update friends list
                if "{CLIENTS}" in message:
                    newclient = message.split("{CLIENTS}")
                    self.refresh_sendlist(newclient[1])
                    self.refresh_friendlist(newclient[1])
                    if not newclient[0][5:] == "":
                        self.show_message(newclient[0][5:], "Clients")
                        self.messageBrowser.moveCursor(QTextCursor.End)
                        # self.scrollRecords.verticalScrollBar().setValue(
                        #     self.scrollRecords.verticalScrollBar().maximum())
                # message type: MESSAGE - receive message
                elif message[:9] == "{MESSAGE}":
                    self.show_message(message[9:], "Message")
                    self.messageBrowser.moveCursor(QTextCursor.End)
                    # self.scrollRecords.verticalScrollBar().setValue(
                    #     self.scrollRecords.verticalScrollBar().maximum())
                elif message[:5] == "{NEW}":
                    self.show_message(message[5:], "NEW")
                elif message[:6] == "{LEFT}":
                    self.show_message(message[6:], "LEFT")
                # message type: None Type - receive private message
                else:
                    self.show_message(message, "Private")
                    self.messageBrowser.moveCursor(QTextCursor.End)
                    # self.scrollRecords.verticalScrollBar().setValue(
                    #     self.scrollRecords.verticalScrollBar().maximum())
            time.sleep(0.1)

    def logout(self, event):
        reply = QtWidgets.QMessageBox.warning(self, u"logout", u"Are you sure to logout?",
                                              QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.disconnect_server()
            # event.accept()
        else:
            event.ignore()

    def connect_server(self, name, IP, port):
        try:
            self.conn.connect((IP, port))
        except:
            self.conn = socket.socket()
            return False
        self.username = name
        # # send to server message type: {LOGIN}
        message = bytes("{LOGIN}" + name, "utf-8")
        self.conn.send(message)
        self.connected = True
        self.rT = threading.Thread(target=self.refresh_interface)
        self.rT.start()
        return True

    def disconnect_server(self):
        if not self.connected:
            return
        # send to server message type: {LOGOUT}
        message = bytes("{LOGOUT}", "utf-8")
        self.conn.send(message)
        # self.connStatus.setText("You are Disconnected")
        # self.nameLineEdit.setReadOnly(False)
        # self.nameLineEdit.clear()
        # close the chat room
        # self.tabs.setTabEnabled(1, False)
        self.connected = False
        self.conn.close()
        self.conn = socket.socket()

    def getMessage(self):
        msg = self.messageTextEdit.toHtml()
        self.messageTextEdit.clear()
        self.messageTextEdit.setFocus()
        return msg

    def sendTowhom(self, sendlist):
        self.sendList = sendlist
        self.sendChoice.setText("Send to: " + sendlist)

    # tools
    def mergeFormatDocumentOrSelection(self, format):
        cursor = self.messageTextEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.Document)

        cursor.mergeCharFormat(format)
        self.messageTextEdit.mergeCurrentCharFormat(format)

    def saveFile(self, fileName):

        SuffixFileName = fileName.split(".")[1]
        if SuffixFileName in ("htm", "html"):
            content = self.messageBrowser.toHtml()
        else:
            content = self.messageBrowser.toPlainText()
        try:
            with codecs.open(fileName, 'w', encoding="gbk") as f:
                f.write(content)
            return True
        except IOError:
            QMessageBox.critical(self, "Error", "Save failed!")
            return False

    @pyqtSlot(str)
    def on_SizeComboBox_currentIndexChanged(self, p0):

        fmt = QTextCharFormat()
        fmt.setFontPointSize(int(p0))
        self.mergeFormatDocumentOrSelection(fmt)
        self.messageTextEdit.setFocus()

    @pyqtSlot(str)
    def on_SizeComboBox1_currentIndexChanged(self, p0):
        self.sendList = p0

    @pyqtSlot(str)
    def on_fontComboBox_currentIndexChanged(self, p0):

        fmt = QTextCharFormat()
        fmt.setFontFamily(p0)
        self.mergeFormatDocumentOrSelection(fmt)

        self.messageTextEdit.setFocus()

    @pyqtSlot(bool)
    def on_boldToolBtn_clicked(self, checked):

        fmt = QTextCharFormat()
        fmt.setFontWeight(checked and QFont.Bold or QFont.Normal)
        self.mergeFormatDocumentOrSelection(fmt)

        self.messageTextEdit.setFocus()

    @pyqtSlot(bool)
    def on_italicToolBtn_clicked(self, checked):

        fmt = QTextCharFormat()
        fmt.setFontItalic(checked)
        self.mergeFormatDocumentOrSelection(fmt)

        self.messageTextEdit.setFocus()

    @pyqtSlot(bool)
    def on_underlineToolBtn_clicked(self, checked):

        fmt = QTextCharFormat()
        fmt.setFontUnderline(checked)
        self.mergeFormatDocumentOrSelection(fmt)
        self.messageTextEdit.setFocus()

    @pyqtSlot(bool)
    def on_colorToolBtn_clicked(self):

        col = QColorDialog.getColor(self.messageTextEdit.textColor(), self)
        if not col.isValid():
            return
        fmt = QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatDocumentOrSelection(fmt)
        self.messageTextEdit.setFocus()

    @pyqtSlot()
    def on_saveToolBtn_clicked(self):

        if self.messageBrowser.document().isEmpty():
            QMessageBox.warning(
                self, "Warning", "The records are NULL!", QMessageBox.Ok)
        else:
            fileName = QFileDialog.getSaveFileName(
                self, "Save chat records", "./chat_records", ("ODT files (*.odt);;HTML-Files (*.htm *.html)"))
            if fileName[0]:
                if self.saveFile(fileName[0]):
                    QMessageBox.information(
                        self, "Save chat records", "Save successfully!")

    @pyqtSlot()
    def on_clearToolBtn_clicked(self):

        self.messageBrowser.clear()

    @pyqtSlot()
    def on_sendButton_clicked(self):

        self.send_message()

    @pyqtSlot()
    def on_exitButton_clicked(self):
        self.disconnect_server()
        self.close()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, u"shutdown", u"Are you sure to leave?",
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.disconnect_server()  # disconnect to server before exit
            event.accept()
        else:
            event.ignore()


userlists = []

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ChatWidget = ChatWidget()
    ChatWidget.show()
    sys.exit(app.exec_())
