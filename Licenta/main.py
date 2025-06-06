import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from UI.mainWindow import Ui_MainWindow
from MainScript.preset_logic import PresetForm  # fereastra care se deschide la "Create"

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Conectezi butonul "Create" la funcția ta
        self.ui.createNewPreset.clicked.connect(self.open_preset_form)

    def open_preset_form(self):
        self.preset_window = PresetForm()
        self.preset_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
