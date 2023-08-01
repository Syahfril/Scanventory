import ast
import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap, QImage, QColor, QTextBlockFormat
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from deteksi4_4 import detect
import json
import mysql.connector
import asset_rc
import time
from PyQt5.QtCore import QTimer


# Load the Qt Designer .ui file
Ui_MainWindow, QtBaseClass = uic.loadUiType("untitled7.ui")

class DetectWindow (QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        
        #button
        self.capture_button.clicked.connect(self.auto)
        self.submit_button.clicked.connect(self.submit_pushed)
        

        #table
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(('Jenis Barang','Jumlah Barang','Tenggat Waktu'))
        header = self.tableWidget.horizontalHeader()
        header.setMinimumSectionSize(200)
        header.setMaximumSectionSize(200)

        horizontal_header = self.tableWidget.horizontalHeader()
        horizontal_header.setStyleSheet("QHeaderView::section { background-color: #2D3A4C; }")

        vertical_header = self.tableWidget.verticalHeader()
        vertical_header.setStyleSheet("QHeaderView::section { background-color: #2D3A4C; }")

        #output
        self.results = []

        #combobox
        self.comboBox = self.findChild(QtWidgets.QComboBox, "comboBox")
        for i in range(10):
            if cv2.VideoCapture(i).isOpened():
                self.comboBox.addItem(f"Camera {i}")
        self.comboBox.setCurrentIndex(0)
        self.comboBox.currentIndexChanged.connect(self.change_camera)

 
    def initialize_camera(self):
        self.cv_cam = detect()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def change_camera(self, index):
        self.cv_cam.change_camera(index)


    def update_frame(self):
        frame = self.cv_cam.capture()
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame, width, height, bytesPerLine, QImage.Format_RGB888)
        self.imgLabel.setPixmap(QPixmap.fromImage(qImg))
        self.imgLabel.setGeometry(QtCore.QRect(0, 0, width, height))
        self.imgLabel.setScaledContents(True)

    def auto(self):
        self.auto_timer = QtCore.QTimer(self)
        self.auto_timer.timeout.connect(self.capture_pushed)
        self.auto_timer.start(5000)
            
    def capture_pushed(self):
        result = self.cv_cam.count_object_in_frame()
        self.results.extend(result)
        self.tableWidget.setRowCount(len(self.results))
        for i, d in enumerate(self.results):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(d["object"]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(d["count"])))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(d["time"]))
      

    def clear_table(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()
            

    def submit_pushed(self):
        self.mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database = "deteksi"
        )

        
        cursor = self.mydb.cursor()
        query = "INSERT INTO item (item_name, item_count, timestamp, user_id) VALUES (%s, %s, %s, %s)"
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i, 0)
            if item is not None:
                item_name = item.text()
                item_count = self.tableWidget.item(i, 1).text()
                timestamp = self.tableWidget.item(i, 2).text()
                user_id = self.labelID.text()
                cursor.execute(query, (item_name, item_count, timestamp, user_id))
            else:
                # Handle the case where the item is None
                self.clear_table()
                return
        print("submited")
        self.mydb.commit()
        cursor.close()
        self.mydb.close()
        self.clear_table()



    



