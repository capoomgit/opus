import sys, os
import time
import gc

try:
    os.add_dll_directory("C:\\Program Files\\Side Effects Software\\Houdini 19.5.368\\bin")
except Exception:
    print("DLL directory could not be added")
    sys.exit()


import threading
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QTimer)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from slave import CapoomSlave
from consts import ClientStatus
import os, json, sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(291, 125)
        self.button_settings = QAction(MainWindow)
        self.button_settings.setObjectName(u"button_settings")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 271, 431))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.comboBox = QComboBox(self.verticalLayoutWidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout.addWidget(self.comboBox)

        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 291, 22))
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuSettings.menuAction())
        self.menuSettings.addAction(self.button_settings)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Capoom Client", None))
        self.button_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Status:", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Online", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Do not disturb", None))

        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        # Remove close button
        MainWindow.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint)

    def __init__(self):
        self.client = None
        self.client_thread = None
        self.client_status = None
        self.setupUi(MainWindow)
        self.retranslateUi(MainWindow)
        self.init_buttons()


        # Start timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start(1000)

    def init_client(self):
        self.client = CapoomSlave(self.get_settings())

        self.client_update_thread = threading.Thread(target=self.client.check_do_update)
        self.client_update_thread.start()

        self.client.connect()

        self.client_garbage_collector = threading.Thread(target=self.collect_garbage)
        self.client_garbage_collector.start()

        self.client_comm_thread = threading.Thread(target=self.client.communicate_with_server)
        self.client_comm_thread.start()


        self.client_thread = threading.Thread(target=self.client.run)
        self.client_thread.start()

    def init_buttons(self):
        self.pushButton.clicked.connect(self.set_status)

        # Exit
        app.aboutToQuit.connect(self.exit)

    def set_status(self):
        self.client_status = self.comboBox.currentText()

        if self.client_status == "Online":
            self.client.set_desired_status(ClientStatus.AVAILABLE.value)
        elif self.client_status == "Do not disturb":
            self.client.set_desired_status(ClientStatus.DND.value)
    
    def collect_garbage(self):
        # This is...
        while True:
            try:
                gc.collect()
            except Exception as e:
                print(e)
            time.sleep(600)

    def exit(self):
        os._exit(1)
        
    def get_settings(self):
        settings = {}
        try:
            settings_file = open(f"{os.getcwd()}/settings.json", "r")
            settings = json.loads(settings_file.read())
        except Exception as e:
            print(e)
            settings = {}

        return settings
    
    def update(self):
        # Check if we just got disconnected or we need update
        if self.client.running == False:
            print("Client disconnected")
            self.client = None
            self.client_thread = None
    
    

# Main
if __name__ == "__main__":
    darkstyle = open(f"P:\pipeline\standalone_dev\libs\darkstyle.qss", "r").read()
    app = QApplication(sys.argv)
    app.setStyleSheet(darkstyle)

    QFontDatabase.addApplicationFont('P:\\pipeline\\standalone_dev\\libs\\fonts\\Larsseit\\Larsseit-Bold.otf')
    app.setFont(QFont("Larsseit-Bold", 10))
    
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    MainWindow.showMinimized()
    ui.init_client()
    sys.exit(app.exec())
