import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QListWidget, QListWidgetItem
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt, QFile, QTextStream

class ChecklistApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the central widget
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create a horizontal layout for the add item widget
        add_item_layout = QHBoxLayout()

        # Create a label and line edit for the item name
        item_name_label = QLabel("Item name:")
        self.item_name_edit = QLineEdit()

        # Create a button to add the item to the checklist
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_item)

        # Add the widgets to the add item layout
        add_item_layout.addWidget(item_name_label)
        add_item_layout.addWidget(self.item_name_edit)
        add_item_layout.addWidget(add_button)

        # Add the add item layout to the main layout
        layout.addLayout(add_item_layout)

        # Create a list widget to display the checklist items
        self.list_widget = QListWidget()
        self.list_widget.itemChanged.connect(self.item_checked)

        # Add the list widget to the main layout
        layout.addWidget(self.list_widget)

        # Load the checklist items from a file
        self.load_items()

    def add_item(self):
        # Get the item name from the line edit
        item_name = self.item_name_edit.text()

        # Create a new item for the list widget
        item = QListWidgetItem(item_name)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Unchecked)

        # Add the item to the list widget
        self.list_widget.addItem(item)

        # Clear the line edit
        self.item_name_edit.clear()

        # Save the checklist items to a file
        self.save_items()

    def item_checked(self, item):
        # Set the text color of checked items to red
        if item.checkState() == Qt.Checked:
            brush = QBrush(QColor("red"))
            item.setForeground(brush)
        else:
            brush = QBrush(QColor("black"))
            item.setForeground(brush)

        # Save the checklist items to a file
        self.save_items()

    def load_items(self):
    # Load the checklist items from a file
        file = QFile("checklist.txt")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            while not stream.atEnd():
                item_name = stream.readLine().strip()
                item = QListWidgetItem(item_name)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                if item_name.endswith("(checked)"):
                    item.setCheckState(Qt.Checked)
                    brush = QBrush(QColor("red"))
                    item.setForeground(brush)
                    item_name = item_name[:-10]  # remove "(checked)" from the end of the text
                    item.setText(item_name)
                else:
                    item.setCheckState(Qt.Unchecked)
                self.list_widget.addItem(item)
            file.close()

    def save_items(self):
        # Save the checklist items to a file
        file = QFile("checklist.txt")
        if file.open(QFile.WriteOnly | QFile.Text):
            stream = QTextStream(file)
            for i in range(self.list_widget.count()):
                item = self.list_widget.item(i)
                if item.checkState() == Qt.Checked:
                    stream << item.text() + " (checked)\n"
                else:
                    stream << item.text() + "\n"
            file.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    checklist_app = ChecklistApp()
    checklist_app.show()
    sys.exit(app.exec_())
