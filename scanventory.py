from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QMessageBox
from addEmp import addEmp, get_shop_for_emp
from dash import get_table_data
from login import do_login
from report import delete_report, get_report, print_table_all_item
from shop import delete_shop, get_shop
from signin import signin
from deteksi8_4 import DetectWindow
from print_item import get_table_item, print_table_item, delete_item


import datetime

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QtWidgets.QStackedWidget(self)

        
        # Login
        self.login = uic.loadUi("login.ui")
        self.stacked_widget.addWidget(self.login)
        self.login.label_4.mousePressEvent = self.switch_to_signin
        self.login.submitButton.clicked.connect(self.login_process)

        #other
        self.other = uic.loadUi("other.ui")
        self.stacked_widget.addWidget(self.other)

        # Sign in
        self.signin = uic.loadUi("signin.ui")
        self.stacked_widget.addWidget(self.signin)
        self.signin.Button_Signin.clicked.connect(self.do_signin)
        self.signin.backButt.mousePressEvent = self.switch_to_login

        #dashboard
        self.dash = uic.loadUi("dashboard.ui")
        self.stacked_widget.addWidget(self.dash)
        self.dash.add_shop.clicked.connect(self.switch_to_shop)
        self.dash.tableShop = self.findChild(QTableWidget, 'tableShop')
        self.dash.deleteButton.clicked.connect(self.delete_shop)
        self.dash.exitButton.clicked.connect(self.go_to_login)
        self.dash.addEmp.clicked.connect(self.switch_to_addEmp)
        self.dash.reportButton.clicked.connect(self.switch_to_report)


        #report
        self.report = uic.loadUi("report.ui")
        self.stacked_widget.addWidget(self.report)
        self.report.exitButton_2.clicked.connect(self.switch_to_dash)
        self.report.deleteButton.clicked.connect(self.delete_report)

        #add employee
        self.addEmp = uic.loadUi("addEmp.ui")
        self.stacked_widget.addWidget(self.addEmp)
        #self.addEmp.Button_addEmp.clicked.connect(self.do_addEmp)
        
        #addShop
        self.addShop = uic.loadUi("shop_add.ui")
        self.stacked_widget.addWidget(self.addShop)
        self.addShop.addButton.clicked.connect(self.do_add_shop)
        self.addShop.backButt.mousePressEvent = lambda event: self.switch_to_dash()

        #main
        self.detect = DetectWindow()
        self.stacked_widget.addWidget(self.detect)
        self.detect.printButton.clicked.connect(self.switch_to_print)
        self.detect.exitButton.clicked.connect(self.switch_to_dash)

        
        #print
        self.print = uic.loadUi("print.ui")
        self.stacked_widget.addWidget(self.print)
        self.print.detectButton.clicked.connect(self.start_detection)
        #self.print.exitButton.clicked.connect(self.switch_to_dash)
        self.print.itemTable = self.findChild(QTableWidget,'itemTable')
  
        self.print.deleteButton.clicked.connect(self.delete_item)
        
        
        # Central
        self.setCentralWidget(self.stacked_widget)


    def get_greeting(self, username):
        current_time = datetime.datetime.now().time()
        if current_time.hour < 12:
            greeting = "Selamat Pagi"
        elif current_time.hour < 18:
            greeting = "Selamat Siang"
        else:
            greeting = "Selamat Malam"
        return f"{greeting}, {username}"

    def login_process(self, event):
        username = self.login.lineEdit_username.text()
        password = self.login.lineEdit_password.text()
        if not username or not password:
            QMessageBox.warning(self.login, "Login Gagal", "Mohon mengisi password dan username")
            return
        result = do_login(username, password)
        if result:
            id_user, role_id = result
            self.id_user = id_user
            print("Role:", role_id)
            if role_id == 1:
                self.start_detection()
                self.detect.labelID.setText(str(id_user))
            elif role_id == 2:
                self.switch_to_dash()    
                greeting = self.get_greeting(username)
                self.dash.label_name.setText(greeting)
                self.dash.user_id.setText(str(id_user))
                self.display_table_shop(id_user)
            
            
            #self.display_report(id_user)
        else:
            QMessageBox.warning(self.login, "Login Gagal", "Username atau password salah")
            
    def go_to_login(self):
        self.stacked_widget.setCurrentWidget(self.login)
    
    def switch_to_login(self,event):
        self.stacked_widget.setCurrentWidget(self.login)

    def switch_to_dash_from_text(self,event):
        self.stacked_widget.setCurrentWidget(self.dash)

    def switch_to_report(self):
        self.stacked_widget.setCurrentWidget(self.report)
        self.display_report()
        
            
    def switch_to_dash(self):
        self.stacked_widget.setCurrentWidget(self.dash)

    def switch_to_other(self):
        self.stacked_widget.setCurrentWidget(self.other)

    def switch_to_signin(self, event):
        self.stacked_widget.setCurrentWidget(self.signin)

    def switch_to_addEmp(self):
        self.stacked_widget.setCurrentWidget(self.addEmp)
        id_user = self.dash.user_id.text()
        self.shop_list = get_shop_for_emp(id_user)
        for shop_id, shop_name in self.shop_list:
            self.addEmp.shopBox.addItem(shop_name, userData=shop_id)
        self.addEmp.shopBox.currentIndexChanged.connect(
            lambda index: self.set_selected_shop_id(self.addEmp.shopBox.itemData(index))
        )
        self.addEmp.Button_addEmp.clicked.connect(self.do_addEmp)

    def set_selected_shop_id(self, shop_id):
        self.selected_shop_id = shop_id        

    def switch_to_shop(self):
        self.stacked_widget.setCurrentWidget(self.addShop)

    def do_signin(self):
        name = self.signin.lineEdit_name.text()
        telp = self.signin.lineEdit_telp.text()
        username = self.signin.lineEdit_username.text()
        password = self.signin.lineEdit_password.text()
        role_id = 2
        result = signin(name, telp, username, password,role_id)

        if result:
            self.stacked_widget.setCurrentWidget(self.login)
        else:
            QMessageBox.warning(self.signin, "Data Kosong","Semua Kolom Harus Diisi")
            self.signin.lineEdit_name.clear()
            self.signin.lineEdit_telp.clear()
            self.signin.lineEdit_username.clear()
            self.signin.lineEdit_password.clear()

    def switch_to_print(self):
        self.stacked_widget.setCurrentWidget(self.print)
        user_id = self.detect.labelID.text()
        # Refresh the table data
        self.display_table_item(user_id)

    def start_detection(self):
        self.detect.initialize_camera()
        self.stacked_widget.setCurrentWidget(self.detect)
    
    def do_add_shop(self):
        name = self.addShop.lineEdit_shopName.text()
        adress = self.addShop.lineEdit_shopAds.text()
        email = self.addShop.lineEdit_email.text()
        phone = self.addShop.lineEdit_phone.text()
        user_id = self.id_user
        
        result = get_shop(name,adress,email,phone,user_id)
        if result:
            # Refresh the table widget with the updated data
            self.display_table_shop(user_id)
            # Clear the line edit fields
            self.addShop.lineEdit_shopName.clear()
            self.addShop.lineEdit_shopAds.clear()
            self.addShop.lineEdit_email.clear()
            self.addShop.lineEdit_phone.clear()
            # Switch back to the dashboard
            self.stacked_widget.setCurrentWidget(self.dash)
        else:
            self.addShop.lineEdit_shopName.clear()
            self.addShop.lineEdit_shopAds.clear()
            self.addShop.lineEdit_email.clear()
            self.addShop.lineEdit_phone.clear()


    def delete_shop(self):
        selected_row = self.dash.tableShop.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self.dash, "Data Kosong", "Plih data untuk dihapus")
            return
        id_shop = int(self.dash.tableShop.item(selected_row, 0).text())
        
        if self.dash.tableShop.rowCount() == 0:
            QMessageBox.warning(self.dash, "Data Kososng", "Tidak ada data yang dihapus")
            return
        delete_shop(id_shop)
        self.dash.tableShop.removeRow(selected_row)

    def do_addEmp(self):
        name = self.addEmp.lineEdit_name_3.text()
        telp = self.addEmp.lineEdit_telp_3.text()
        username = self.addEmp.lineEdit_username_3.text()
        password = self.addEmp.lineEdit_password_3.text()
        role_id = 1
        shop_id = self.selected_shop_id
        result = addEmp(name, telp, username, password,shop_id, role_id)

        if result:
            self.stacked_widget.setCurrentWidget(self.login)
        else:
            QMessageBox.warning(self.signin, "Data Kosong","Semua Kolom Harus Diisi")
            self.signin.lineEdit_name.clear()
            self.signin.lineEdit_telp.clear()
            self.signin.lineEdit_username.clear()
            self.signin.lineEdit_password.clear()
        
            
    def display_report(self):
        
        def update_table():
            timestamp_filter = self.report.comboReport.currentText()
            user_id = self.id_user
            data, column_names = get_report("item",user_id, timestamp_filter)

            if not data:
                self.report.reportTable.setColumnCount(1)
                self.report.reportTable.setHorizontalHeaderLabels(["'Data empty'"])
                self.report.reportTable.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #092133; }")
            else:
                self.report.reportTable.setRowCount(len(data))
                self.report.reportTable.setColumnCount(len(data[0]))
                self.report.reportTable.setHorizontalHeaderLabels(column_names)
                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        self.report.reportTable.setItem(i, j, item)
                self.report.reportTable.show()
                self.report.reportTable.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #092133; }")
                self.report.reportTable.setHorizontalHeaderLabels(column_names)
                horizontal_header = self.report.reportTable.horizontalHeader()
                horizontal_header.setStyleSheet("QHeaderView::section { background-color: #2D3A4C; }")
                vertical_header = self.report.reportTable.verticalHeader()
                vertical_header.setStyleSheet("QHeaderView::section { background-color: #2D3A4C; }")
                self.report.printButton.clicked.connect(lambda: self.print_all_data(user_id, timestamp_filter))
            

        self.report.comboReport.addItems(["all","Last 1 day", "Last 1 week", "Last 1 month"])
        self.report.comboReport.setCurrentIndex(0)
        self.report.comboReport.currentTextChanged.connect(update_table)
        #self.print.printButton.clicked.connect(lambda: self.print_data(id_shop))
        update_table()

    def display_table_item(self,user_id):

        def update_tables():
            timestamp_filter = self.report.comboReport.currentText()
            data, column_names = get_table_item("item",user_id,timestamp_filter)
            if not data:
                if not data:
                    self.print.itemTable.setColumnCount(1)
                    self.print.itemTable.setHorizontalHeaderLabels(["'Data empty'"])
                    self.print.itemTable.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #092133; }")
                    return

            # self.print.itemTable.setColumnWidth(0, 0)
            # self.print.itemTable.setColumnWidth(4, 0)

            self.print.itemTable.setRowCount(len(data))
            self.print.itemTable.setColumnCount(len(data[0]))
            for i, row in enumerate(data):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.print.itemTable.setItem(i, j, item)

            self.print.itemTable.setHorizontalHeaderLabels(column_names)
            horizontal_header = self.print.itemTable.horizontalHeader()
            horizontal_header.setStyleSheet("QHeaderView::section { background-color: #2D3A4C; }")
            vertical_header = self.print.itemTable.verticalHeader()
            vertical_header.setStyleSheet("QHeaderView::section { background-color: #2D3A4C; }")
            self.print.printButton.clicked.connect(lambda: self.print_data(user_id, timestamp_filter))


        self.print.filterTime.addItems(["all","Last 1 day", "Last 1 week", "Last 1 month"])
        self.print.filterTime.setCurrentIndex(0)
        self.print.filterTime.currentTextChanged.connect(update_tables)
        update_tables()

    def print_all_data(self,user_id, timestamp_filter): 
        filename = "reports.csv"
        print_table_all_item(user_id, filename, timestamp_filter)
        QMessageBox.information(self.print,"","Data Berhasil dicetak")

    def print_data(self,user_id, timestamp_filter): 
        filename = "report.csv"  
        print_table_item(user_id, filename, timestamp_filter)
        QMessageBox.information(self.print,"","Data Berhasil dicetak")

    def delete_item(self):
        selected_row = self.print.itemTable.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self.print, "Data Kosong", "Plih data untuk dihapus")
            return
        id_item = int(self.print.itemTable.item(selected_row, 0).text())
        if self.print.itemTable.rowCount() == 0:
            QMessageBox.warning(self.print, "Data Kosong", "Tidak ada data yang dihapus")
            return
        delete_item("item", id_item)
        self.print.itemTable.removeRow(selected_row)

    def delete_report(self):
        selected_row = self.report.reportTable.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self.report, "Data Kosong", "Plih data untuk dihapus")
            return
        id_item = int(self.report.reportTable.item(selected_row, 0).text())
        if self.report.reportTable.rowCount() == 0:
            QMessageBox.warning(self.report, "Data Kosong", "Tidak ada data yang dihapus")
            return
        delete_report("item", id_item)
        self.report.reportTable.removeRow(selected_row)

    def display_table_shop(self,id_user):
        # Get data from MySQL database
        #id_user = self.dash.user_id.text()
        data, column_names = get_table_data(id_user)
        if not data:
            self.dash.tableShop.setColumnCount(1)
            self.dash.tableShop.setHorizontalHeaderLabels(["'Data empty'"])
            self.dash.tableShop.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #092133; }")
            return

        # Create QTableWidget and populate it with data
        self.dash.tableShop.setRowCount(len(data))
        self.dash.tableShop.setColumnCount(len(data[0]))

        # Hide columns with index 0 and 5
        self.dash.tableShop.setColumnWidth(0, 0)
        self.dash.tableShop.setColumnWidth(5, 0)

        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.dash.tableShop.setItem(i, j, item)


        self.dash.tableShop.setHorizontalHeaderLabels(column_names)
        horizontal_header = self.dash.tableShop.horizontalHeader()
        horizontal_header.setStyleSheet("QHeaderView::section { background-color: #2D3A4C; }")
        vertical_header = self.dash.tableShop.verticalHeader()
        vertical_header.setStyleSheet("QHeaderView::section { background-color: #2D3A4C; }")


    def showEvent(self, event):
        super().showEvent(event)
        self.setWindowState(QtCore.Qt.WindowMaximized)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
