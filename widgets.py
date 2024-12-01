from config import Config, Filter, Target
from PyQt6.QtWidgets import (
    QPushButton, QListWidget, QWidget,
    QListWidgetItem, QDialog, QVBoxLayout,
    QLineEdit, QHBoxLayout, QFileDialog,
    QProgressBar, QLabel
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

QLineEdit_dark_stylesheet = """ QLineEdit { color: white; } """
QLineEdit_light_stylesheet = """ QLineEdit { color: black; } """

class CleaningProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.label = QLabel(self)
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

    def setValue(self, value):
        self.progress_bar.setValue(value)
    
    def setMaximum(self, value):
        self.progress_bar.setMaximum(value)

    def increment(self, value=1):
        self.progress_bar.setValue(self.progress_bar.value() + value)
    
    def decrement(self, value=1):
        self.progress_bar.setValue(self.progress_bar.value() - value)
    
    def setLabelText(self, text):
        self.label.setText(text)

class CustomFilterItem(QListWidgetItem):
    def __init__(self, filter: Filter):
        super().__init__(filter.name)
        self.filter = filter
        super().setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

    def __repr__(self):
        return self.filter.name
class FilterEditorDialog(QDialog):
    def __init__(self, config:Config, filter=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Filter Editor")
        self.filter = filter
        self.config = config

        layout = QVBoxLayout(self)

        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("Filter Name")
        layout.addWidget(self.name_edit)

        self.expressions_list = QListWidget(self)
        layout.addWidget(self.expressions_list)

        self.expression_edit = QLineEdit(self)
        self.expression_edit.setPlaceholderText("Add Expression")
        layout.addWidget(self.expression_edit)

        add_expression_button = QPushButton("Add Expression", self)
        add_expression_button.clicked.connect(self.add_expression)
        layout.addWidget(add_expression_button)

        self.folder_edit = QLineEdit(self)
        self.folder_edit.setPlaceholderText("Folder")
        layout.addWidget(self.folder_edit)

        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save)
        buttons_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        if self.filter:
            self.name_edit.setText(self.filter.name)
            self.folder_edit.setText(self.filter.folder)
            for expression in self.filter.expressions:
                self.expressions_list.addItem(QListWidgetItem(expression))

        # Apply custom stylesheet for QLineEdit widgets
        self.set_stylesheet()

    def set_stylesheet(self):


        stylesheet = QLineEdit_dark_stylesheet if "dark" in self.config.theme else QLineEdit_light_stylesheet
        self.name_edit.setStyleSheet(stylesheet)
        self.expression_edit.setStyleSheet(stylesheet)
        self.folder_edit.setStyleSheet(stylesheet)

    def add_expression(self):
        expression = self.expression_edit.text().strip()
        if expression:
            self.expressions_list.addItem(QListWidgetItem(expression))
            self.expression_edit.clear()

    def save(self):
        name = self.name_edit.text().strip()
        folder = self.folder_edit.text().strip()
        expressions = [self.expressions_list.item(i).text() for i in range(self.expressions_list.count())]

        if name and folder and expressions:
            self.filter = Filter(name, expressions, folder)
            self.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            selected_items = self.expressions_list.selectedItems()
            if not selected_items:
                return
            for item in selected_items:
                self.expressions_list.takeItem(self.expressions_list.row(item))
        else:
            super().keyPressEvent(event)


class CustomTargetItem(QListWidgetItem):
    def __init__(self, target: Target):
        super().__init__(target.name + " - " + target.path)
        self.target = target
        super().setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

    def __repr__(self):
        return self.target.name
    
class TargetEditorDialog(QDialog):
    def __init__(self, config: Config, target=None, parent=None):
        super().__init__(parent)
        self.resize(400, 200)
        self.setWindowTitle("Target Editor")
        self.target = target
        self.config = config

        layout = QVBoxLayout(self)

        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("Target Name")
        layout.addWidget(self.name_edit)

        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit(self)
        self.path_edit.setPlaceholderText("Path")
        path_layout.addWidget(self.path_edit)

        folder_button = QPushButton(self)
        folder_button.setIcon(QIcon.fromTheme("folder"))
        folder_button.clicked.connect(self.select_folder)
        path_layout.addWidget(folder_button)

        layout.addLayout(path_layout)

        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save)
        buttons_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        if self.target:
            self.name_edit.setText(self.target.name)
            self.path_edit.setText(self.target.path)

        # Apply custom stylesheet for QLineEdit widgets
        self.set_stylesheet()

    def set_stylesheet(self):
        stylesheet = QLineEdit_dark_stylesheet if "dark" in self.config.theme else QLineEdit_light_stylesheet
        self.name_edit.setStyleSheet(stylesheet)
        self.path_edit.setStyleSheet(stylesheet)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.path_edit.setText(folder)

    def save(self):
        name = self.name_edit.text().strip()
        path = self.path_edit.text().strip()

        if name and path:
            self.target = Target(name, path)
            self.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self.path_edit.clear()
        else:
            super().keyPressEvent(event)