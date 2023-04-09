import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore
from lab4 import Ui_MainWindow
import sys


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.show()

        self.cap = cv2.VideoCapture('video.mp4')
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # 提取橙色乒乓球的遮罩
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_orange = (6, 100, 100)
        upper_orange = (20, 255, 255)
        mask = cv2.inRange(hsv, lower_orange, upper_orange)

        # 找到乒乓球的轮廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            cnt = max(contours, key=cv2.contourArea)

        # 显示处理结果
        self.showImage(frame, self.label)
        self.showImage(mask, self.label_2)
        self.showImage(cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) & frame, self.label_3)

    def showImage(self, cvImg, qlabel):
        if len(cvImg.shape) == 2:  # 单通道图像
            height, width = cvImg.shape
            bytesPerLine = width
            qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
        else:  # 三通道图像
            height, width, channel = cvImg.shape
            bytesPerLine = 3 * width
            qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        qlabel.setPixmap(QPixmap.fromImage(qImg))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
