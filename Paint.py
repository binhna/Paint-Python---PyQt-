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
        imageSize = QtCore.QSize(1366, 768)
        self.image = QtGui.QImage(imageSize, QtGui.QImage.Format_RGB32)

        self.image.fill(QtGui.qRgb(255, 255, 255))



    def closeEvent(self, event):
        print("Closed")


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QtCore.Qt.red)
        cur_size = QRect(0, 0, self.width(), self.height())
        temp = self.image.copy(cur_size)
        painter.drawImage(event.rect(), temp)
        #painter.drawLine(self.start, self.end)
        _drawCircle(self.start, self.end, self)
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
            _drawCircle(self.start, self.end, self.image)
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


        self.update()

    def drawLineTo(self, end):
        self.update()



def _drawLine(start, end, k):
    p = QPainter(k)
    if start == end:
        p.drawPoint(start)
        return
    import math
    y = start.y()
    x = start.x()
    f = lambda x: int(x + math.modf(x)[0])
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
    p.drawPoint(end)

def _drawRect(start, end, k):
    b = QPoint(end.x(), start.y())
    d = QPoint(start.x(), end.y())
    _drawLine(start, b, k)
    _drawLine(b, end, k)
    _drawLine(start, d, k)
    _drawLine(d, end, k)

def _drawCircle(start, end, k):
    xc = int(abs(end.x() + start.x()) / 2)
    yc = int(abs(end.y() + start.y()) / 2)
    p = QPainter(k)
    def point4(xc, yc, x, y):
        p.drawPoint(x + xc, y + yc)
        p.drawPoint(x + xc, -y + yc)
        p.drawPoint(-x + xc, -y + yc)
        p.drawPoint(-x + xc, y + yc)

    def point8(xc, yc, x, y):
        p.drawPoint(x + xc, y + yc)
        p.drawPoint(-x + xc, y + yc)
        p.drawPoint(x + xc, -y + yc)
        p.drawPoint(-x + xc, -y + yc)
        p.drawPoint(y + xc, x + yc)
        p.drawPoint(-y + xc, x + yc)
        p.drawPoint(y + xc, -x + yc)
        p.drawPoint(-y + xc, -x + yc)

    if abs(end.y() - start.y()) == abs(end.x() - start.x()):
        r = int(abs(end.y() - start.y()) / 2)
        x = 0
        y = r
        f = 1 - r
        point8(xc, yc, x, y)
        while(x < y):
            if (f < 0):
                f += (x<<1) + 3
            else:
                y -= 1
                f += ((x-y)<<1) + 5
            x += 1
            point8(xc, yc, x, y)
    else:
        a = int(abs(end.x() - start.x()) / 2)
        b = int(abs(end.y() - start.y()) / 2)
        if a == 0 or b == 0:
            _drawLine(start, end, k)
            return
        c = float((b**2)/a/a)
        x = 0
        y = b
        point4(xc, yc, x, y)
        q = c*2 - b*2 + 1
        while(y >= c*x):
            if q < 0:
                q += (x*2 + 3)*(c*2)
            else:
                q += (x*2 + 3)*(c*2) + (1-y)*4
                y -= 1
            x += 1
            point4(xc, yc, x, y)
        x = a
        y = 0
        c = float((a**2)/b/b)
        point4(xc,yc,x,y)
        q = c*2 - a*2 + 1
        while(c*y <= x):
            if (q < 0):
                q += (c*2) * (y*2 + 3)
            else:
                q += (c*2) * (y*2 + 3) + (1 - x)*4
                x -= 1
            y += 1
            point4(xc,yc,x,y)

app = QApplication(sys.argv)
form = Widget()
form.show()
app.exec_()





