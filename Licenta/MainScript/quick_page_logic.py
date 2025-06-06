from PyQt6.QtWidgets import QWidget
from UI.quickPage import Ui_Form
from MainScript.preview_page_logic import PreviewPage

class QuickPage(QWidget):
    def __init__(self, project_context):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.context = project_context
        self.profile_names = self.context.profile_names
        self.current_profile = self.profile_names[0] if self.profile_names else None

        # Dicționar local: profil → listă de opțiuni bifate
        self.optimizations_by_profile = {name: [] for name in self.profile_names}

        # Populate UI
        self.ui.profileCombo.clear()
        self.ui.profileCombo.addItems(self.profile_names)
        self.ui.profileCombo.setCurrentIndex(0)
        self.ui.profileCombo.currentIndexChanged.connect(self.on_profile_change)

        self.populate_labels()
        self.load_optimizations(self.current_profile)

        # Butoane
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.cancelButton_2.clicked.connect(self.close)

    def populate_labels(self):
        self.ui.label.setText("Remove Cortana")
        self.ui.label_2.setText("Disable Telemetry")
        self.ui.label_3.setText("Uninstall Default Apps")
        self.ui.label_4.setText("Disable Tracking ID")

        for checkbox in [self.ui.checkBox, self.ui.checkBox_2, self.ui.checkBox_3, self.ui.checkBox_4]:
            checkbox.setChecked(False)

    def on_profile_change(self, index):
        new_profile = self.profile_names[index]

        # Salvează selecțiile curente în dicționarul local
        if self.current_profile:
            self.optimizations_by_profile[self.current_profile] = self.get_selected_options()

        # Încarcă opțiunile pentru noul profil
        saved_opts = self.optimizations_by_profile.get(new_profile, [])
        self.ui.checkBox.setChecked("Remove Cortana" in saved_opts)
        self.ui.checkBox_2.setChecked("Disable Telemetry" in saved_opts)
        self.ui.checkBox_3.setChecked("Uninstall Default Apps" in saved_opts)
        self.ui.checkBox_4.setChecked("Disable Tracking ID" in saved_opts)

        self.current_profile = new_profile

    def get_selected_options(self):
        opts = []
        if self.ui.checkBox.isChecked():
            opts.append("Remove Cortana")
        if self.ui.checkBox_2.isChecked():
            opts.append("Disable Telemetry")
        if self.ui.checkBox_3.isChecked():
            opts.append("Uninstall Default Apps")
        if self.ui.checkBox_4.isChecked():
            opts.append("Disable Tracking ID")
        return opts

    def load_optimizations(self, profile):
        saved_opts = self.optimizations_by_profile.get(profile, [])
        self.ui.checkBox.setChecked("Remove Cortana" in saved_opts)
        self.ui.checkBox_2.setChecked("Disable Telemetry" in saved_opts)
        self.ui.checkBox_3.setChecked("Uninstall Default Apps" in saved_opts)
        self.ui.checkBox_4.setChecked("Disable Tracking ID" in saved_opts)

    def save(self):
        # Salvează opțiunile curente în dicționarul local
        self.optimizations_by_profile[self.current_profile] = self.get_selected_options()

        # Scrie toate opțiunile salvate în context
        for profile, options in self.optimizations_by_profile.items():
            self.context.set_optimizations(profile, options)

        # Deschide preview
        self.preview_window = PreviewPage(project_context=self.context)
        self.preview_window.show()
        self.close()
