from PyQt6.QtWidgets import QWidget, QListView, QMessageBox
from PyQt6.QtCore import QStringListModel
from UI.presetPage import Ui_Form
from MainScript.folder_logic import FolderLogic
from Objects.project_context import ProjectContext

class PresetForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Inițializare listă de profiluri
        self.profile_list = []
        self.model = QStringListModel(self.profile_list)
        self.ui.profilesList.setModel(self.model)

        # Conectăm butoanele
        self.ui.addFolderButton.clicked.connect(self.add_profile)
        self.ui.removeButton.clicked.connect(self.remove_selected_profile)
        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.nextButton.clicked.connect(self.go_to_next)
        self.ui.lockButton.clicked.connect(self.toggle_admin_lock)

        # Flag pentru blocarea administratorului
        self.admin_locked = False

    def add_profile(self):
        profile_name = self.ui.profileNameEdit.text().strip()
        if profile_name:
            self.profile_list.append(profile_name)
            self.model.setStringList(self.profile_list)
            self.ui.profileNameEdit.clear()
        else:
            QMessageBox.warning(self, "Warning", "Introdu un nume de profil!")

    def remove_selected_profile(self):
        selected_indexes = self.ui.profilesList.selectedIndexes()
        if selected_indexes:
            for index in sorted(selected_indexes, reverse=True):
                self.profile_list.pop(index.row())
            self.model.setStringList(self.profile_list)
        else:
            QMessageBox.information(self, "Info", "Selectează un profil de șters.")

    def go_to_next(self):
        preset_name = self.ui.presetNameEdit.text().strip()
        if not preset_name:
            QMessageBox.warning(self, "Warning", "Introduceți un nume de preset!")
            return

        if not self.profile_list:
            QMessageBox.warning(self, "Warning", "Adăugați cel puțin un profil!")
            return

        # 🟢 Deschide următoarea fereastră cu lista de profiluri
        context = ProjectContext(profile_names=self.profile_list)
        self.nextWindow = FolderLogic(project_context=context)
        self.nextWindow.show()
        self.close()

    def toggle_admin_lock(self):
        name = self.ui.adminProfileEdit.text().strip()

        if not self.admin_locked:
            if not name:
                QMessageBox.warning(self, "Warning", "Introduceți un nume pentru profilul administratorului!")
                return
            # Activează blocarea
            self.ui.adminProfileEdit.setReadOnly(True)
            self.ui.lockButton.setText("Unlock")
            if name in self.profile_list:
                self.profile_list.remove(name)
            self.profile_list.insert(0, name)
            self.model.setStringList(self.profile_list)
            self.admin_locked = True
        else:
            # Deblochează câmpul și elimină numele din listă
            self.ui.adminProfileEdit.setReadOnly(False)
            self.ui.lockButton.setText("Lock")
            name = self.ui.adminProfileEdit.text().strip()
            if name in self.profile_list:
                self.profile_list.remove(name)
            self.model.setStringList(self.profile_list)
            self.admin_locked = False
