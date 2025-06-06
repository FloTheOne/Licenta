from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(937, 679)

        MainWindow.setStyleSheet("""
        QWidget {
            background-color: #66A5AD;
            color: #002629;
            font-family: Segoe UI, Arial;
            font-size: 14px;
        }

        QGroupBox {
            border: 1px solid #e1ebf0;
            border-radius: 8px;
            margin-top: 24px;
            font-weight: bold;
            color: #e1ebf0;
        }
                                 
        QStatusBar {
        background-color: transparent;
        border: none;
        }                                    

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 4px 12px;
            color: #002629;
            margin-bottom: 4px;
        }

        QPushButton {
            background-color: #e1ebf0;
            color: #002629;
            border: none;
            padding: 8px 20px;
            border-radius: 10px;
            font-weight: bold;
            min-width: 100px;
        }

        QPushButton:hover {
            background-color: #B3DDE4;
        }

        QListView {
            background-color: #e1ebf0;
            border: 1px solid #e1ebf0;
            border-radius: 6px;
            padding: 4px;
        }


        QMenuBar {
            background-color: #e1ebf0;
            color: #002629;
        }

        QMenuBar::item:selected {
            background: #B3DDE4;
        }
        """)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # === Presets list and Setup panel ===
        centerLayout = QtWidgets.QHBoxLayout()

        self.viewPresets = QtWidgets.QListView()
        self.viewPresets.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        centerLayout.addWidget(self.viewPresets)

        self.groupBoxSetup = QtWidgets.QGroupBox("Setups")
        setupLayout = QtWidgets.QVBoxLayout(self.groupBoxSetup)

        buttonGrid = QtWidgets.QGridLayout()
        self.runButton = QtWidgets.QPushButton("Run")
        self.editButton = QtWidgets.QPushButton("Edit")
        self.importButton = QtWidgets.QPushButton("Import")
        self.deleteButton = QtWidgets.QPushButton("Delete")

        buttonGrid.addWidget(self.runButton, 0, 0)
        buttonGrid.addWidget(self.editButton, 0, 1)
        buttonGrid.addWidget(self.importButton, 1, 0)
        buttonGrid.addWidget(self.deleteButton, 1, 1)

        setupLayout.addStretch()
        setupLayout.addLayout(buttonGrid)

        centerLayout.addWidget(self.groupBoxSetup)

        mainLayout.addLayout(centerLayout)

        # === Bottom Buttons ===
        bottomLayout = QtWidgets.QHBoxLayout()
        self.createNewPreset = QtWidgets.QPushButton("Create")
        self.quickSettingsButton = QtWidgets.QPushButton("Quick Settings")
        bottomLayout.addStretch()
        bottomLayout.addWidget(self.createNewPreset)
        bottomLayout.addSpacing(20)
        bottomLayout.addWidget(self.quickSettingsButton)
        bottomLayout.addStretch()

        mainLayout.addSpacing(20)
        mainLayout.addLayout(bottomLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 937, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))