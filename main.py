import sys
from ui import MainWindow
from config import Config
from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet, list_themes

app = QApplication(sys.argv)

config = Config()
window = MainWindow(app=app, config=config)

theme = config.theme if config.theme and config.theme in list_themes() else 'dark_blue.xml'

apply_stylesheet(app, theme=config.theme)

window.show()
app.exec()