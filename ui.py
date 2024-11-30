from pathlib import Path
import sys

from config import Config
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow, QPushButton, 
    QGridLayout, QWidget,
    QTabWidget, QListWidget,
    QVBoxLayout, QAbstractItemView,
    QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from widgets import CustomFilterItem, FilterEditorDialog, CustomTargetItem, TargetEditorDialog
from qt_material import apply_stylesheet, list_themes

QComboBox_dark_stylesheet = """ QComboBox { color: white; padding: 5px; } """
QComboBox_light_stylesheet = """ QComboBox { color: black; padding: 5px; } """

class MainWindow(QMainWindow):
    singleton: 'MainWindow' = None
    
    def __init__(self, app: QApplication, config: Config):
        super().__init__()
        MainWindow.singleton = self
        
        self.resize(640, 480)
        self.setWindowIcon(QIcon(str(self._get_icon_path())))
        self.setWindowTitle("Folder Cleaner")
        self.app = app
        self.config = config

        self._setupMenuBars()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QGridLayout(central_widget)
        central_widget.setLayout(main_layout)

        tab = QTabWidget(self)
        main_layout.addWidget(tab, 0, 0)

        self.home_tab = MainWindowTab(self, config)
        tab.addTab(self.home_tab, "Home")

        self.filters_tab = FiltersTab(self, config)
        tab.addTab(self.filters_tab, "Filters")

        self.targets_tab = TargetsTab(self, config)
        tab.addTab(self.targets_tab, "Targets")

        self.theme_tab = ThemeTab(self, config)
        tab.addTab(self.theme_tab, "Theme")

    def _get_icon_path(self):
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle (e.g., with PyInstaller)
            return str(Path(sys._MEIPASS) / 'icon.png')
        else:
            # If the application is run as a script
            return str(Path(__file__).parent / 'icon.png')

    def _setupMenuBars(self):
        menu_bar = self.menuBar()

        save_action = menu_bar.addAction("Save")
        save_action.triggered.connect(self.config.save)

        load_action = menu_bar.addAction("Load")
        load_action.triggered.connect(self._load_config)

    def _load_config(self):
        self.config.load()
        theme = self.config.theme if self.config.theme and self.config.theme in list_themes() else 'dark_blue.xml'
        self.config.theme = theme
        self.config.save()

        apply_stylesheet(self.app, theme=self.config.theme)
        self.filters_tab._update_filters()
        self.targets_tab._update_targets()
        self.theme_tab.theme_dropdown.setCurrentText(self.config.theme)

    @staticmethod
    def restart():
        MainWindow.singleton = MainWindow(MainWindow.singleton.app, MainWindow.singleton.config)

class MainWindowTab(QWidget):
    def __init__(self, parent: MainWindow, config: Config):
        super().__init__()
        self.config = config

        layout = QGridLayout(self)
        self.setLayout(layout)

        clean_button = QPushButton("Clean Folders", self)
        layout.addWidget(clean_button, 0, 0)
        clean_button.clicked.connect(self.clean_folders)

    def clean_folders(self):
        print("Cleaning folders")

        for target in self.config.targets:
            print(f"Cleaning {target}")

        print("Done cleaning folders")

class FiltersTab(QWidget):
    def __init__(self, parent: MainWindow, config: Config):
        super().__init__()
        self.config = config

        main_layout = QGridLayout(self)
        self.setLayout(main_layout)

        self.filter_list = QListWidget(self)
        self.filter_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.filter_list.itemDoubleClicked.connect(self.edit_filter)

        for filter in self.config.filters:
            item = CustomFilterItem(filter)
            self.filter_list.addItem(item)

        main_layout.addWidget(self.filter_list, 0, 0, 1, 1)

        buttons_layout = QVBoxLayout()
        main_layout.addLayout(buttons_layout, 0, 1)

        add_filter_button = QPushButton("Add Filter", self)
        add_filter_button.clicked.connect(self.add_filter)
        buttons_layout.addWidget(add_filter_button)

        move_up_button = QPushButton("Move Up", self)
        move_up_button.clicked.connect(self.move_up)
        buttons_layout.addWidget(move_up_button)

        move_down_button = QPushButton("Move Down", self)
        move_down_button.clicked.connect(self.move_down)
        buttons_layout.addWidget(move_down_button)

        buttons_layout.addStretch()

    def add_filter(self):
        dialog = FilterEditorDialog(config=self.config, parent=self)
        if dialog.exec():
            new_filter = dialog.filter
            self.config.filters.append(new_filter)
            self._update_filters()
            self.config.save()

    def edit_filter(self, item):
        filter = item.filter
        dialog = FilterEditorDialog(config=self.config, filter=filter, parent=self)
        if dialog.exec():
            updated_filter = dialog.filter
            index = self.config.filters.index(filter)
            self.config.filters[index] = updated_filter
            self._update_filters()
            self.config.save()

    def move_up(self):
        current_row = self.filter_list.currentRow()
        if current_row > 0:
            current_item = self.filter_list.takeItem(current_row)
            self.filter_list.insertItem(current_row - 1, current_item)
            self.filter_list.setCurrentRow(current_row - 1)
            self._save_filters()

    def move_down(self):
        current_row = self.filter_list.currentRow()
        if current_row < self.filter_list.count() - 1:
            current_item = self.filter_list.takeItem(current_row)
            self.filter_list.insertItem(current_row + 1, current_item)
            self.filter_list.setCurrentRow(current_row + 1)
            self._save_filters()

    def _update_filters(self):
        self.filter_list.clear()
        for filter in self.config.filters:
            item = CustomFilterItem(filter)
            self.filter_list.addItem(item)

    def _save_filters(self):
        self.config.filters = [self.filter_list.item(i).filter for i in range(self.filter_list.count())]
        self.config.save()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            selected_items = self.filter_list.selectedItems()
            if not selected_items:
                return
            for item in selected_items:
                self.filter_list.takeItem(self.filter_list.row(item))
            self._save_filters()
        else:
            super().keyPressEvent(event)

class TargetsTab(QWidget):
    def __init__(self, parent: MainWindow, config: Config):
        super().__init__()
        self.config = config

        main_layout = QGridLayout(self)
        self.setLayout(main_layout)

        self.target_list = QListWidget(self)
        self.target_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.target_list.itemDoubleClicked.connect(self.edit_target)

        for target in self.config.targets:
            item = CustomTargetItem(target)
            self.target_list.addItem(item)

        main_layout.addWidget(self.target_list, 0, 0, 1, 1)

        buttons_layout = QVBoxLayout()
        main_layout.addLayout(buttons_layout, 0, 1)

        add_target_button = QPushButton("Add Target", self)
        add_target_button.clicked.connect(self.add_target)
        buttons_layout.addWidget(add_target_button)

        move_up_button = QPushButton("Move Up", self)
        move_up_button.clicked.connect(self.move_up)
        buttons_layout.addWidget(move_up_button)

        move_down_button = QPushButton("Move Down", self)
        move_down_button.clicked.connect(self.move_down)
        buttons_layout.addWidget(move_down_button)

        buttons_layout.addStretch()

    def add_target(self):
        dialog = TargetEditorDialog(config=self.config, parent=self)
        if dialog.exec():
            new_target = dialog.target
            self.config.targets.append(new_target)
            self._update_targets()
            self.config.save()

    def edit_target(self, item):
        target = item.target
        dialog = TargetEditorDialog(config=self.config, target=target, parent=self)
        if dialog.exec():
            updated_target = dialog.target
            index = self.config.targets.index(target)
            self.config.targets[index] = updated_target
            self._update_targets()
            self.config.save()

    def move_up(self):
        current_row = self.target_list.currentRow()
        if current_row > 0:
            current_item = self.target_list.takeItem(current_row)
            self.target_list.insertItem(current_row - 1, current_item)
            self.target_list.setCurrentRow(current_row - 1)
            self._save_targets()

    def move_down(self):
        current_row = self.target_list.currentRow()
        if current_row < self.target_list.count() - 1:
            current_item = self.target_list.takeItem(current_row)
            self.target_list.insertItem(current_row + 1, current_item)
            self.target_list.setCurrentRow(current_row + 1)
            self._save_targets()

    def _update_targets(self):
        self.target_list.clear()
        for target in self.config.targets:
            item = CustomTargetItem(target)
            self.target_list.addItem(item)

    def _save_targets(self):
        self.config.targets = [self.target_list.item(i).target for i in range(self.target_list.count())]
        self.config.save()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            selected_items = self.target_list.selectedItems()
            if not selected_items:
                return
            for item in selected_items:
                self.target_list.takeItem(self.target_list.row(item))
            self._save_targets()
        else:
            super().keyPressEvent(event)

class ThemeTab(QWidget):
    def __init__(self, parent: MainWindow, config: Config):
        super().__init__()
        self.config = config
        self.mainWindow = parent

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Make a simple dropdown to select the theme
        themes = list_themes()
        self.theme_dropdown = QComboBox(self)

        self.theme_dropdown.setStyleSheet(self._QComboBox_stylesheet())

        self.theme_dropdown.addItems(themes)
        self.theme_dropdown.setCurrentText(self.config.theme)
        layout.addWidget(self.theme_dropdown)

        apply_button = QPushButton("Apply", self)
        apply_button.clicked.connect(self.apply_theme)
        layout.addWidget(apply_button)

    def apply_theme(self):
        theme = self.theme_dropdown.currentText()
        self.config.theme = theme
        self.config.save()
        print(f"Applying theme: {theme}")
        apply_stylesheet(self.mainWindow.app, theme=theme)
        self.theme_dropdown.setStyleSheet(self._QComboBox_stylesheet())

    def _QComboBox_stylesheet(self):
        return QComboBox_dark_stylesheet if "dark" in self.config.theme else QComboBox_light_stylesheet