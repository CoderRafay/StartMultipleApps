import os
import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QPushButton, QLabel, QComboBox, QLineEdit, QMessageBox, QInputDialog

CONFIG_FILE = "app_modes_config.json"

class AppModeConfigurator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_config()

    def initUI(self):
        self.setWindowTitle("App Mode Configurator")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        self.mode_label = QLabel("Select Mode:")
        layout.addWidget(self.mode_label)

        self.mode_combo_box = QComboBox()
        layout.addWidget(self.mode_combo_box)

        self.listbox_apps = QListWidget()
        layout.addWidget(self.listbox_apps)

        self.button_add = QPushButton("Add App")
        self.button_add.clicked.connect(self.add_app)
        layout.addWidget(self.button_add)

        self.button_remove = QPushButton("Remove Selected App")
        self.button_remove.clicked.connect(self.remove_app)
        layout.addWidget(self.button_remove)

        self.button_launch = QPushButton("Launch Mode")
        self.button_launch.clicked.connect(self.launch_apps)
        layout.addWidget(self.button_launch)

        self.button_add_mode = QPushButton("Add Mode")
        self.button_add_mode.clicked.connect(self.add_mode)
        layout.addWidget(self.button_add_mode)

        self.button_edit_mode = QPushButton("Edit Mode")
        self.button_edit_mode.clicked.connect(self.edit_mode)
        layout.addWidget(self.button_edit_mode)

        self.button_delete_mode = QPushButton("Delete Mode")
        self.button_delete_mode.clicked.connect(self.delete_mode)
        layout.addWidget(self.button_delete_mode)

        self.central_widget.setLayout(layout)

        self.mode_combo_box.currentIndexChanged.connect(self.update_listbox)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                app_modes = json.load(f)
                self.app_modes = app_modes
                self.mode_combo_box.addItems(app_modes.keys())
                self.update_listbox()
        else:
            self.app_modes = {}

    def save_config(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.app_modes, f)

    def add_app(self):
        mode = self.mode_combo_box.currentText()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select App", "", "Executable Files (*.exe)")
        if file_path:
            self.app_modes[mode].append(file_path)
            self.update_listbox()

    def remove_app(self):
        mode = self.mode_combo_box.currentText()
        selected_items = self.listbox_apps.selectedItems()
        for item in selected_items:
            self.app_modes[mode].remove(item.text())
        self.update_listbox()

    def launch_apps(self):
        mode = self.mode_combo_box.currentText()
        app_paths = self.app_modes[mode]
        for app_path in app_paths:
            os.startfile(app_path)

    def update_listbox(self):
        mode = self.mode_combo_box.currentText()
        self.listbox_apps.clear()
        self.listbox_apps.addItems(self.app_modes[mode])

    def add_mode(self):
        mode_name, ok = QInputDialog.getText(self, "Add Mode", "Enter Mode Name:")
        if ok and mode_name.strip() != "":
            self.app_modes[mode_name] = []
            self.mode_combo_box.addItem(mode_name)

    def edit_mode(self):
        current_mode = self.mode_combo_box.currentText()
        new_mode_name, ok = QInputDialog.getText(self, "Edit Mode", "Enter New Mode Name:", QLineEdit.Normal, current_mode)
        if ok and new_mode_name.strip() != "":
            self.app_modes[new_mode_name] = self.app_modes.pop(current_mode)
            index = self.mode_combo_box.findText(new_mode_name)
            self.mode_combo_box.setItemText(index, new_mode_name)

    def delete_mode(self):
        current_mode = self.mode_combo_box.currentText()
        reply = QMessageBox.question(self, "Delete Mode", f"Are you sure you want to delete '{current_mode}' mode?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.app_modes.pop(current_mode)
            index = self.mode_combo_box.findText(current_mode)
            self.mode_combo_box.removeItem(index)

    def closeEvent(self, event):
        self.save_config()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppModeConfigurator()
    window.show()
    sys.exit(app.exec_())
