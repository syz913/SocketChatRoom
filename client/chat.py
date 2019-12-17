import socket
import sys
import codecs
import threading
import time
import re
import sqlite3
import win32ui
import struct
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt, QProcess, QDateTime, QFile, QTextStream
from PyQt5.QtGui import QFont, QColor, QTextCursor, QTextCharFormat, QTextDocumentWriter
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QFileDialog, QColorDialog, QHeaderView, QApplication, QMenu, QAction
from Ui_Form.Ui_chat import Ui_chat
import client
import DataBase

class ChatWidget(QtWidgets.QWidget, Ui_chat):
    def __init__(self, parent=None):
        super(ChatWidget, self).__init__(parent)
        self.setupUi(self)
        self.setWindowOpacity(1)
        self.networkInit()
        # self.sendButton.clicked.connect(self.send("TEXT"))
        self.exitButton.clicked.connect(self.logout)
        # Automatically adjusts the column width with the window size
        self.userTableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        # Automatically adjusts the row height with the window size
        self.userTableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
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
    
    def messageInit(self):
        conn = sqlite3.connect("socketdb.db")
        cursor = conn.execute("select * from messages where owner = '" + self.username + "'")
        for messages in cursor:
            username = messages[1]
            date = messages[2]
            message = messages[3]
            type = messages[4]
            self.init_messgae(username, message, date, type)
        conn.close()
        self.messageBrowser.setAlignment(Qt.AlignCenter)
        self.messageBrowser.setTextColor(Qt.gray)
        self.messageBrowser.setCurrentFont(QFont("Times New Roman", 10))
        self.messageBrowser.append("--- Above is chat history ---")
        self.messageBrowser.append(" ")

    def show_message(self, newMessage, type):
        times = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        username = ""
        message = ""
        try:
            username = newMessage.split(" : ")[0]
            message = newMessage.split(" : ")[1]
        except:
            pass
        if type == "Message":
            if username == self.username:
                message = self.handleMessage(message, 1)
                self.messageBrowser.setAlignment(Qt.AlignRight)
            else:
                message = self.handleMessage(message, 0)
                self.messageBrowser.setAlignment(Qt.AlignLeft)
            DataBase.save_message(self.username, username, times, message, "Message")
            # print(message)
            self.messageBrowser.setTextColor(Qt.blue)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 12))
            self.messageBrowser.append("[" + username + "]  " + times)
            self.messageBrowser.append(message)
            # self.messageBrowser.append("😍😙")
            self.messageBrowser.append(" ")
        elif type == "Private":
            if username == "{PRIVATE}" + self.username:
                message = self.handleMessage(message, 1)
                self.messageBrowser.setAlignment(Qt.AlignRight)
            else:
                message = self.handleMessage(message, 0)
                self.messageBrowser.setAlignment(Qt.AlignLeft)
            DataBase.save_message(self.username, username, times, message, "Private")
            self.messageBrowser.setTextColor(Qt.red)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 12))
            self.messageBrowser.append("[" + username + "]  " + times)
            self.messageBrowser.append(message)
            self.messageBrowser.append(" ")
        if type == "FILE":
            if username == self.username:
                self.messageBrowser.setAlignment(Qt.AlignRight)
            else:
                self.messageBrowser.setAlignment(Qt.AlignLeft)
            DataBase.save_message(self.username, username, times, message, "FILE")
            self.messageBrowser.setTextColor(Qt.blue)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 12))
            self.messageBrowser.append("[" + username + "]  " + times)
            fileName = re.findall(".*src=\"(.*)\">", message)[0][15:]
            self.messageBrowser.setTextColor(Qt.gray)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 8))
            if self.isImg(fileName):
                self.messageBrowser.append(" ")
                self.messageBrowser.append(message)
                self.messageBrowser.append(" ")
            else:
                self.messageBrowser.append("<img src=\"./client/materials/pdf.png\">")
                self.messageBrowser.append(fileName)
                self.messageBrowser.append(" ")
        if type == "PRIVATEFILE":
            if username == self.username:
                self.messageBrowser.setAlignment(Qt.AlignRight)
            else:
                self.messageBrowser.setAlignment(Qt.AlignLeft)
            DataBase.save_message(self.username, username, times, message, "FILE")
            self.messageBrowser.setTextColor(Qt.red)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 12))
            self.messageBrowser.append("[{Private}" + username + "]  " + times)
            fileName = re.findall(".*src=\"(.*)\">", message)[0][15:]
            self.messageBrowser.setTextColor(Qt.gray)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 8))
            if self.isImg(fileName):
                self.messageBrowser.append(" ")
                self.messageBrowser.append(message)
                self.messageBrowser.append(" ")
            else:
                self.messageBrowser.append("<img src=\"./client/materials/pdf.png\">")
                self.messageBrowser.append(fileName)
                self.messageBrowser.append(" ")
        if type == "NEW":
            self.messageBrowser.setAlignment(Qt.AlignCenter)
            self.messageBrowser.setTextColor(Qt.gray)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 10))
            self.messageBrowser.append(newMessage + "  " + times)
            self.messageBrowser.append(" ")
        if type == "LEFT":
            self.messageBrowser.setAlignment(Qt.AlignCenter)
            self.messageBrowser.setTextColor(Qt.gray)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 10))
            self.messageBrowser.append(newMessage + "  " + times)
            self.messageBrowser.append(" ")
        time.sleep(0.2)
        # self.scrollRecords.verticalScrollBar().setValue(
        #     self.scrollRecords.verticalScrollBar().maximum())

    def init_messgae(self, username, message, times, type):
        if type == "Message":
            if username == self.username:
                self.messageBrowser.setAlignment(Qt.AlignRight)
            else:
                self.messageBrowser.setAlignment(Qt.AlignLeft)
            # print(message)
            self.messageBrowser.setTextColor(Qt.blue)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 12))
            self.messageBrowser.append("[" + username + "]  " + times)
            self.messageBrowser.append(message)
            self.messageBrowser.append(" ")
        elif type == "Private":
            if username == "{PRIVATE}" + self.username:
                self.messageBrowser.setAlignment(Qt.AlignRight)
            else:
                self.messageBrowser.setAlignment(Qt.AlignLeft)
            self.messageBrowser.setTextColor(Qt.red)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 12))
            self.messageBrowser.append("[" + username + "]  " + times)
            self.messageBrowser.append(message)
            self.messageBrowser.append(" ")
        elif type == "FILE":
            if username == self.username:
                self.messageBrowser.setAlignment(Qt.AlignRight)
            else:
                self.messageBrowser.setAlignment(Qt.AlignLeft)
            self.messageBrowser.setTextColor(Qt.blue)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 12))
            self.messageBrowser.append("[" + username + "]  " + times)
            fileName = re.findall(".*src=\"(.*)\">", message)[0][15:]
            self.messageBrowser.setTextColor(Qt.gray)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 8))
            if self.isImg(fileName):
                self.messageBrowser.append(" ")
                self.messageBrowser.append(message)
                self.messageBrowser.append(" ")
            else:
                self.messageBrowser.append("<img src=\"./client/materials/pdf.png\">")
                self.messageBrowser.append(fileName)
                self.messageBrowser.append(" ")
        elif type == "PRIVATEFILE":
            if username == self.username:
                self.messageBrowser.setAlignment(Qt.AlignRight)
            else:
                self.messageBrowser.setAlignment(Qt.AlignLeft)
            self.messageBrowser.setTextColor(Qt.red)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 12))
            self.messageBrowser.append("[{Private}" + username + "]  " + times)
            fileName = re.findall(".*src=\"(.*)\">", message)[0][15:]
            self.messageBrowser.setTextColor(Qt.gray)
            self.messageBrowser.setCurrentFont(QFont("Times New Roman", 8))
            if self.isImg(fileName):
                self.messageBrowser.append(" ")
                self.messageBrowser.append(message)
                self.messageBrowser.append(" ")
            else:
                self.messageBrowser.append("<img src=\"./client/materials/pdf.png\">")
                self.messageBrowser.append(fileName)
                self.messageBrowser.append(" ")

    def send_message(self, type):
        if type == "TEXT":
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
        elif type == "FILE":
            if os.path.isfile(self.filepath):
                # # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
                # fileinfo_size = struct.calcsize('128sl')
                # 定义文件头信息，包含文件名和文件大小
                fhead = struct.pack(
                        '128sl',
                        os.path.basename(self.filepath).encode(encoding="utf-8"),
                        os.stat(self.filepath).st_size)
                print('client filepath: {0}'.format(self.filepath))
                self.conn.sendall(fhead)                    
                fp = open(self.filepath, 'rb')
                while True:
                    data = fp.read(1024)
                    if not data:
                        self.conn.sendall(bytes(self.sendList + "|" + self.username, "utf-8"))
                        print('file send over...')
                        break
                    self.conn.sendall(data)

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
            # print("index:" + user)
            isOnline = users.index(user) if (user in users) else -1
            font = QFont("Playball", 16)
            if isOnline == -1:
                user = QTableWidgetItem(user+" ("+"off-line"+")")
                user.setFont(font)
                self.userTableWidget.insertRow(0)
                self.userTableWidget.setItem(0, 0, user)
            else:
                user = QTableWidgetItem(user+" ("+"online"+")")
                user.setFont(font)
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
            self.SizeComboBox1.setCurrentIndex(0)

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
                elif message[:6] == "{FILE}":
                    self.show_message(message[6:], "FILE")
                    self.messageBrowser.moveCursor(QTextCursor.End)
                elif message[:13] == "{PRIVATEFILE}":
                    self.show_message(message[13:], "PRIVATEFILE")
                    self.messageBrowser.moveCursor(QTextCursor.End)
                # message type: None Type - receive private message
                else:
                    self.show_message(message, "Private")
                    self.messageBrowser.moveCursor(QTextCursor.End)
                    # self.scrollRecords.verticalScrollBar().setValue(
                    #     self.scrollRecords.verticalScrollBar().maximum())
            time.sleep(0.1)

    def connect_server(self, name, IP, port):
        try:
            self.conn.connect((IP, port))
        except:
            self.conn = socket.socket()
            return False
        self.username = name
        self.messageInit()
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
        # add enter
        msg = self.messageTextEdit.toHtml()
        self.messageTextEdit.clear()
        self.messageTextEdit.setFocus()
        return msg

    # alter the CSS, but QTextBrowser don't support many attributes
    def handleMessage(self, msg, type):
        style1 = " style = \"background:rgb(145,237,97); width:fit-content; padding:10px;\
                border:1px solid gray;line-height:30px; border-radius:6px;"
        style2 = " style = \"background:rgb(204, 204, 204); width:fit-content; padding:10px;\
                border:1px solid gray;line-height:300%; border-radius:6px;"
        style_base = re.findall(".*<span style=\" (.*)\">", msg)
        messages = msg.split("<style type=\"text/css\">")
        if len(style_base) == 0:
            words = re.findall(".*;\">(.*)</p>.*", messages[1])
        else:
            words = re.findall(".*;\">(.*)</span>.*", messages[1])
        message = " "
        for word in words:
            if word != "<br />":
                message += word
        # self
        if type == 1:
            if len(style_base) == 0:
                msg = messages[0] + style1 + "</head><body>" + "<p><span" + style1 + "\">" + message + " </span></p></body></html>"
            else:
                msg = messages[0] + style1 + "</head><body>" + "<p><span" + style1 + style_base[0] + "\">" + message + " </span></p></body></html>"
        # others
        else:
            if len(style_base) == 0:
                msg = messages[0] + style2 + "</head><body>" + "<p><span" + style2 + "\">" + message + " </span></p></body></html>"
            else:
                msg = messages[0] + style2 + "</head><body>" + "<p><span" + style2 + style_base[0] + "\">" + message + " </span></p></body></html>"
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
            with codecs.open(fileName, 'w', encoding="utf8") as f:
                f.write(content)
            return True
        except IOError:
            QMessageBox.critical(self, "Error", "Save failed!")
            return False

    def isImg(self, str):
        is_img = False
        if ".jpg" in str:
            is_img = True
        elif ".png" in str:
            is_img = True
        elif ".jpeg" in str:
            is_img = True
        return is_img

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
    def on_imageBtn_clicked(self, checked):

        dlg = win32ui.CreateFileDialog(1)  # 1 means open the file dialog box
        dlg.SetOFNInitialDir('C:/')  # initial directory
        dlg.DoModal()
        self.filepath = dlg.GetPathName()  # Get the name of the selected file
        # self.messageTextEdit.append("<img src=\""+self.filepath+"\">")
        print(self.filepath)
        self.send("FILE")

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

        self.send("TEXT")

    # @pyqtSlot()
    def send(self, type):

        self.send_message(type)

    def logout(self):
        reply = QtWidgets.QMessageBox.warning(self, u"logout", u"Are you sure to logout?",
                                              QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
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

    # keyboard events
    def keyPressEvent(self, event):
        # event.key（）display the code
        # print("press: " + str(event.key()))
        if (event.key() == Qt.Key_Escape):
            self.logout()
        if (event.key() + 1 == Qt.Key_Enter):
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.send("TEXT")
            else:
                print("enter")


userlists = []

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ChatWidget = ChatWidget()
    ChatWidget.show()
    sys.exit(app.exec_())
