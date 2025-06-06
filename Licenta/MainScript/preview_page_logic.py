from PyQt6.QtWidgets import QWidget, QTextEdit, QPushButton, QVBoxLayout, QMessageBox
import json

class PreviewPage(QWidget):
    def __init__(self, project_context):
        super().__init__()
        self.setWindowTitle("Preview Config")
        self.resize(700, 500)

        self.context = project_context
        self.data = self.context.get_all()

        # UI
        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)

        self.save_button = QPushButton("Save Config")
        self.save_button.clicked.connect(self.save_config)

        layout = QVBoxLayout()
        layout.addWidget(self.text_preview)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

        self.build_preview()

    def build_preview(self):
        lines = []
        for profile, config in self.data.items():
            lines.append(f"🟦 Profil: {profile}")
            lines.append("📁 Folders:")
            lines.append(json.dumps(config["folders"], indent=2))
            lines.append("🛠 Optimizations:")
            lines.append(json.dumps(config["optimizations"], indent=2))
            lines.append("-" * 60)

        lines.append("🗂 Structură foldere aplicații (global):")
        lines.append(json.dumps(self.context.get_apps_structure(), indent=2))
        lines.append("📦 Aplicații globale:")
        lines.append(json.dumps(self.context.get_apps_global(), indent=2))

        self.text_preview.setPlainText("\n".join(lines))

    def save_config(self):
        try:
            export_data = {
                "profiles": self.data,
                "apps_structure": self.context.get_apps_structure(),
                "apps_global": self.context.get_apps_global()
            }
            with open("preset_config.json", "w") as f:
                json.dump(export_data, f, indent=4)
            QMessageBox.information(self, "Success", "Config saved to preset_config.json!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save config: {str(e)}")
