import copy
from io import BytesIO

from PyQt5 import QtCore
from win32clipboard import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Bbox(object):
    def __init__(self):
        self._x1, self._y1 = 0, 0
        self._x2, self._y2 = 0, 0

    @property
    def point1(self):
        return self._x1, self._y1

    @point1.setter
    def point1(self, position: tuple):
        self._x1 = position[0]
        self._y1 = position[1]

    @property
    def point2(self):
        return self._x2, self._y2

    @point2.setter
    def point2(self, position: tuple):
        self._empty = False
        self._x2 = position[0]
        self._y2 = position[1]

    @property
    def bbox(self):
        if self._x1 < self._x2:
            x_min, x_max = self._x1, self._x2
        else:
            x_min, x_max = self._x2, self._x1

        if self._y1 < self._y2:
            y_min, y_max = self._y1, self._y2
        else:
            y_min, y_max = self._y2, self._y1
        return (x_min, y_min, x_max - x_min, y_max - y_min)

    def __str__(self):
        return str(self.bbox)


class ScreenLabel(QLabel):
    signal = pyqtSignal(QRect)

    def __init__(self):
        super().__init__()
        self._press_flag = False
        self._bbox = Bbox()
        self._pen = QPen(Qt.white, 2, Qt.DashLine)
        self._painter = QPainter()
        self._bbox = Bbox()
        desktop = QApplication.desktop()
        global_cursor_screen = desktop.screenNumber(QCursor.pos())
        screen = desktop.screenGeometry(global_cursor_screen)
        width, height = screen.width(), screen.height()

        self.width_limit = width//2
        self.height_limit = height//2


        self._pixmap = QPixmap(width, height)
        self._pixmap.fill(QColor(255, 255, 255))
        self.setPixmap(self._pixmap)
        self.setWindowOpacity(0.4)

        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置背景颜色为透明
        QShortcut(QKeySequence("esc"), self, self.close)

        # self.setWindowFlag(Qt.Tool)  # 不然exec_执行退出后整个程序退出


    def _draw_bbox(self):
        pixmap = self._pixmap.copy()
        self._painter.begin(pixmap)
        self._painter.setPen(self._pen)  # 设置pen必须在begin后
        rect = QRect(*self._bbox.bbox)
        self._painter.fillRect(rect, Qt.SolidPattern)  # 区域不透明
        self._painter.drawRect(rect)  # 绘制虚线框
        self._painter.end()
        self.setPixmap(pixmap)
        self.update()
        self.showFullScreen()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            # print("鼠标左键：", [QMouseEvent.x(), QMouseEvent.y()])
            self._press_flag = True
            self._bbox.point1 = [QMouseEvent.x(), QMouseEvent.y()]

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton and self._press_flag:
            # print("鼠标释放：", [QMouseEvent.x(), QMouseEvent.y()])
            self._bbox.point2 = [QMouseEvent.x(), QMouseEvent.y()]
            self._press_flag = False
            # if the box is too big, ignore it
            if self._bbox.point2[0] - self._bbox.point1[0] > self.width_limit or\
                 self._bbox.point2[1] - self._bbox.point1[1] > self.height_limit:
                print("[INFO] THE BOX IS TOO BIG, IGNORE IT")
                return
            self.signal.emit(QRect(*self._bbox.bbox))

    def mouseMoveEvent(self, QMouseEvent):
        if self._press_flag:
            # print("鼠标移动：", [QMouseEvent.x(), QMouseEvent.y()])
            self._bbox.point2 = [QMouseEvent.x(), QMouseEvent.y()]
            self._draw_bbox()


class SimpleScreenShot(QWidget):
    def __init__(self) -> None:
        super().__init__()

    def simple_screen_shot(self):
        desktop = QApplication.desktop()
        global_cursor_screen = desktop.screenNumber(QCursor.pos())
        screen = desktop.screenGeometry(global_cursor_screen)

        self.label = ScreenLabel()
        self.label.setGeometry(screen)
        # self.label.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.label.showNormal()
        self.label.showFullScreen()
        self.label.signal.connect(self.callback)
    
    def get_shot_img(self, rect):
        desktop = QApplication.desktop()
        global_cursor_screen = desktop.screenNumber(QCursor.pos())
        screen = QApplication.screens()[global_cursor_screen]

        return screen.grabWindow(0).copy(rect).toImage()


    def get_shot_bytes(self, rect):
        shot_bytes = QByteArray()
        buffer = QBuffer(shot_bytes)
        buffer.open(QIODevice.WriteOnly)
        shot_img = self.get_shot_img(rect)
        shot_img.save(buffer, 'png')
        return shot_bytes.data()


    def callback(self, pixmap):
        """截图完成回调函数"""
        self.label.close()
        del self.label  # del前必须先close
        # dialog = ShotDialog(pixmap)
        # self.img = copy.deepcopy(dialog.get_shot_bytes())
        # dialog.exec_()
        self.img = self.get_shot_bytes(pixmap)
        self.close()
    
    def close(self) -> bool:
        return super().close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = SimpleScreenShot()
    window.simple_screen_shot()
    sys.exit(app.exec_())
