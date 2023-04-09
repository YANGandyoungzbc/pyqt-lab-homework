from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from lab3 import Ui_MainWindow


class VideoPlayer(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.fps_flag = ''
        self.current_frame = None
        self.timer = QtCore.QTimer(self)

        self.pushButton.clicked.connect(self.play_video)
        self.pushButton_2.clicked.connect(self.stop_video)

    def play_video(self):
        if self.fps_flag == '':
            start_frame = int(self.lineEdit.text())
        else:
            start_frame = int(self.fps_flag)

        # Open video file
        self.cap = cv2.VideoCapture("video.mp4")

        # Set start frame
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        # Get video properties
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))

        # Start timer to display frames
        self.timer.timeout.connect(self.next_frame)
        self.timer.start(int(1000 / fps))  # 1000ms/fps

        # Update label for FPS
        self.label_3.setText(f"Fps: {fps}")

        # Update label for starting frame number
        self.label_2.setText(f"起始帧号：{start_frame}")

        # Enable stop button
        self.pushButton_2.setEnabled(True)

    def stop_video(self):
        self.fps_flag = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        self.timer.stop()
        self.cap.release()

    def next_frame(self):
        ret, frame = self.cap.read()

        if ret:
            # Convert frame to QImage
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
            self.current_frame = q_img

            # Get current frame number
            current_frame_number = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

            # Add current frame number to the video frame
            cv2.putText(rgb_image, f"Current: {current_frame_number}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                        thickness=2)

            # Show frame in label
            self.label.setPixmap(QtGui.QPixmap.fromImage(q_img))

            # Update label for current frame number
            self.label_2.setText(f"当前帧号：{current_frame_number}")
        else:
            # Stop timer and release video capture
            self.timer.stop()
            self.cap.release()

            # Disable stop button
            self.pushButton_2.setEnabled(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = VideoPlayer()
    window.show()
    app.exec_()
