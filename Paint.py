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
        #painter.drawLine(self.start, self.end)
        #_drawLine(self.start, self.end, self)
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
            #painter = QPainter(self.image)
            #painter.drawLine(self.start, self.end)
            _drawLine(self.start, self.end, self.image)
            self.update()
            self.keepDraw = False
        #self.x0 = self.y0 = -1
        #self.update()

    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton) and self.keepDraw:
            self.end = event.pos()
            #_drawLine(self.start,self.end,self)
            #p = QPainter(self.image)
            #p.drawLine(self.start, self.end)
            _drawLine(self.start, self.end, self.image)
            self.start = self.end
        self.update()

    def drawLineTo(self, end):
        self.update()

    def resizeEvent(self, event):
        self.resizeImage(self.image, event.size())
        super(Widget, self).resizeEvent(event)

    def resizeImage(self, image, newSize):
        #print("ccc")
        if image.size() == newSize:
            return
        newImage = QtGui.QImage(newSize, QtGui.QImage.Format_RGB32)
        newImage.fill(QtGui.qRgb(255, 255, 255))
        painter = QtGui.QPainter(newImage)
        painter.drawImage(QtCore.QPoint(0, 0), image)
        self.image = newImage


def _drawLine(start, end, k):
    if start == end:
        return
    import math
    y = start.y()
    x = start.x()
    f = lambda x: int(x + math.modf(x)[0])
    p = QPainter(k)
    if (end.x() - start.x()) != 0:
        m = ((end.y() - start.y()) / (end.x() - start.x()))
        b = start.y() - m * start.x()
        if(abs(m) > 1):
            temph = (end.y() - start.y()) / abs(end.y() - start.y())
            while (y != end.y()):
                x = f((y - b) / m)
                p.drawPoint(x, (y))
                y += temph
        elif(abs(m) >= 0):
            tempw = (end.x() - start.x()) / abs(end.x() - start.x())
            while (x != end.x()):
                y = f(x * m + b)
                p.drawPoint(x, y)
                x += tempw
    else:
        temph = (end.y() - start.y()) / abs(end.y() - start.y())
        while (y != end.y()):
            p.drawPoint(x, y)
            y += temph

def _drawRect(start, end, k):
    b = QPoint(end.x(), start.y())
    d = QPoint(start.x(), end.y())


app = QApplication(sys.argv)
form = Widget()
form.show()
app.exec_()





