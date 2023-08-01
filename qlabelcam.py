import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import cv2
import numpy as np
from process import detect

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = QLabel()
        self.setCentralWidget(self.label)

        self.cv_processor = detect()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame) # Connect the timeout signal to update_frame method
        self.timer.start(30) # Start the timer with 30 millisecond interval
        

        #self.cap = cv2.VideoCapture(0)

    def update_frame(self):
        
        # Your function that was running inside the OpenCV loop
        frame = self.cv_processor.capture() 
        
        #height, width, channel = frame.shape
        bytesPerLine = 3 * 640
        qImg = QImage(frame, 640, 480, bytesPerLine, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qImg))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
