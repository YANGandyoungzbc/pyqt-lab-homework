import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore
from coin import Ui_MainWindow
import sys


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.show()

        self.coin_counter = 0
        self.cap = cv2.VideoCapture('coin04.mp4')
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # 提取硬币的遮罩
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_orange = (0, 0, 221)
        upper_orange = (180, 30, 255)
        mask = cv2.inRange(hsv, lower_orange, upper_orange)

        # 找到硬币轮廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            cnt = max(contours, key=cv2.contourArea)

        # 计算硬币的位置
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 标记硬币的位置
        cv2.circle(frame, (x + w // 2, y + h // 2), 10, (0, 0, 255), -1)

        # 给被标记的硬币添加一个编号
        cv2.putText(frame, str(self.coin_counter + 1), (x + w // 2, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2)

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
