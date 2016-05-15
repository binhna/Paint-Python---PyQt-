
import sys
import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Widget(QWidget):

    def __init__(self):
        super(Widget, self).__init__()
        self.layout = QVBoxLayout()
        self.keepDraw = False
        self.start = QPoint()
        self.end = QPoint()
        self.resize(400, 300)
        self.move(100, 100)
        self.setWindowTitle("Events")
        self.image = QImage()

    def closeEvent(self, event):
        print("Closed")


    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setPen(QtCore.Qt.red)
        painter.drawImage(event.rect(), self.image)
        painter.drawLine(self.start, self.end)
        self.update()
            #painter.restore()
            #self.render(self)
            #self.update()



    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.keepDraw = True
            self.start = self.end = event.pos()
            #print(self.start)
        #self.update()


    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.keepDraw:
            painter = QPainter(self.image)
            painter.drawLine(self.start, self.end)
            self.update()
            self.keepDraw = False
        #self.x0 = self.y0 = -1
        #self.update()

    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton) and self.keepDraw:
            self.end = event.pos()
        #self.update()

    def drawLineTo(self, end):
        self.update()

    def resizeEvent(self, event):
        self.resizeImage(self.image, event.size())
        super(Widget, self).resizeEvent(event)

    def resizeImage(self, image, newSize):
        print("ccc")
        if image.size() == newSize:
            return
        newImage = QtGui.QImage(newSize, QtGui.QImage.Format_RGB32)
        newImage.fill(QtGui.qRgb(255, 255, 255))
        painter = QtGui.QPainter(newImage)
        painter.drawImage(QtCore.QPoint(0, 0), image)
        self.image = newImage

app = QApplication(sys.argv)
form = Widget()
form.show()
app.exec_()

