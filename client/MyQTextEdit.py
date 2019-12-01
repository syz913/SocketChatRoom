from PyQt5 import QtCore, QtWidgets

#参考链接：https://blog.csdn.net/u010909667/article/details/53576053
class MyQTextEdit(QtWidgets.QTextEdit):
    def __init__(self):
         super(MyQTextEdit,self).__init__()
         self.zoomsize=2
         self.ctrlPressed=False
    def wheelEvent(self, event):#this is the rewrite of the function
       if  self.ctrlPressed:    #if the ctrl key is pressed: then deal with the defined process
          delta=event.angleDelta()
          oriention= delta.y()/8
          self.zoomsize=0
          if oriention>0:
                self.zoomsize+=1
          else:
                 self.zoomsize-=1
          self.zoomIn(self.zoomsize)
          print(self.zoomsize)
       else:   #if the ctrl key isn't pressed then submiting                   the event to it's super class
          return super().wheelEvent(event)

    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key()==QtCore.Qt.Key_Control:
            self.ctrlPressed=False
        return super().keyReleaseEvent(QKeyEvent)
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key()==QtCore.Qt.Key_Control:
            self.ctrlPressed=True
            print("The ctrl key is holding down")
        return super().keyPressEvent(QKeyEvent)