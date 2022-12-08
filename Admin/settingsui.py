import json

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsALLKgq.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_dialog_settings(object):
    def setupUi(self, dialog_settings):
        if not dialog_settings.objectName():
            dialog_settings.setObjectName(u"dialog_settings")
        dialog_settings.resize(469, 507)
        self.horizontalLayoutWidget_2 = QWidget(dialog_settings)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(50, 450, 371, 51))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.button_save = QPushButton(self.horizontalLayoutWidget_2)
        self.button_save.setObjectName(u"button_save")

        self.horizontalLayout_2.addWidget(self.button_save)

        self.button_close = QPushButton(self.horizontalLayoutWidget_2)
        self.button_close.setObjectName(u"button_close")

        self.horizontalLayout_2.addWidget(self.button_close)

        self.verticalLayoutWidget = QWidget(dialog_settings)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 448, 431))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.verticalLayoutWidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_8)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_3.addWidget(self.label_2)

        self.input_serverip = QLineEdit(self.verticalLayoutWidget)
        self.input_serverip.setObjectName(u"input_serverip")

        self.horizontalLayout_3.addWidget(self.input_serverip)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.label)

        self.input_serverport = QLineEdit(self.verticalLayoutWidget)
        self.input_serverport.setObjectName(u"input_serverport")

        self.horizontalLayout.addWidget(self.input_serverport)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_9 = QLabel(self.verticalLayoutWidget)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_9)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_4.addWidget(self.label_3)

        self.input_dbusrname = QLineEdit(self.verticalLayoutWidget)
        self.input_dbusrname.setObjectName(u"input_dbusrname")

        self.horizontalLayout_4.addWidget(self.input_dbusrname)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_5.addWidget(self.label_4)

        self.input_dbpass = QLineEdit(self.verticalLayoutWidget)
        self.input_dbpass.setObjectName(u"input_dbpass")

        self.horizontalLayout_5.addWidget(self.input_dbpass)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_6.addWidget(self.label_5)

        self.input_dbname = QLineEdit(self.verticalLayoutWidget)
        self.input_dbname.setObjectName(u"input_dbname")

        self.horizontalLayout_6.addWidget(self.input_dbname)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_6 = QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_7.addWidget(self.label_6)

        self.input_dbhost = QLineEdit(self.verticalLayoutWidget)
        self.input_dbhost.setObjectName(u"input_dbhost")

        self.horizontalLayout_7.addWidget(self.input_dbhost)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_7 = QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_8.addWidget(self.label_7)

        self.input_dbport = QLineEdit(self.verticalLayoutWidget)
        self.input_dbport.setObjectName(u"input_dbport")

        self.horizontalLayout_8.addWidget(self.input_dbport)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.label_10 = QLabel(self.verticalLayoutWidget)
        self.label_10.setObjectName(u"label_10")
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_10)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_11 = QLabel(self.verticalLayoutWidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_9.addWidget(self.label_11)

        self.input_googlewebhook = QLineEdit(self.verticalLayoutWidget)
        self.input_googlewebhook.setObjectName(u"input_googlewebhook")

        self.horizontalLayout_9.addWidget(self.input_googlewebhook)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_12 = QLabel(self.verticalLayoutWidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_10.addWidget(self.label_12)

        self.input_settingspath = QLineEdit(self.verticalLayoutWidget)
        self.input_settingspath.setObjectName(u"input_settingspath")

        self.horizontalLayout_10.addWidget(self.input_settingspath)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_13 = QLabel(self.verticalLayoutWidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_11.addWidget(self.label_13)

        self.input_omnisettings = QLineEdit(self.verticalLayoutWidget)
        self.input_omnisettings.setObjectName(u"input_omnisettings")

        self.horizontalLayout_11.addWidget(self.input_omnisettings)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(dialog_settings)

        QMetaObject.connectSlotsByName(dialog_settings)

    # setupUi

    def retranslateUi(self, dialog_settings):
        dialog_settings.setWindowTitle(QCoreApplication.translate("dialog_settings", u"Dialog", None))
        self.button_save.setText(QCoreApplication.translate("dialog_settings", u"Save", None))
        self.button_close.setText(QCoreApplication.translate("dialog_settings", u"Close w/o saving", None))
        self.label_8.setText(QCoreApplication.translate("dialog_settings", u"TCP Settings", None))
        self.label_2.setText(QCoreApplication.translate("dialog_settings", u"Server IP", None))
        self.input_serverip.setText(QCoreApplication.translate("dialog_settings", u"1.1.1.1", None))
        self.label.setText(QCoreApplication.translate("dialog_settings", u"Server Port", None))
        self.input_serverport.setText(QCoreApplication.translate("dialog_settings", u"1234", None))
        self.label_9.setText(QCoreApplication.translate("dialog_settings", u"Database Settings", None))
        self.label_3.setText(QCoreApplication.translate("dialog_settings", u"Database Username", None))
        self.input_dbusrname.setText(QCoreApplication.translate("dialog_settings", u"user", None))
        self.label_4.setText(QCoreApplication.translate("dialog_settings", u"Database Password", None))
        self.input_dbpass.setText(QCoreApplication.translate("dialog_settings", u"password", None))
        self.label_5.setText(QCoreApplication.translate("dialog_settings", u"Database Name", None))
        self.input_dbname.setText(QCoreApplication.translate("dialog_settings", u"dbname", None))
        self.label_6.setText(QCoreApplication.translate("dialog_settings", u"Database IP", None))
        self.input_dbhost.setText(QCoreApplication.translate("dialog_settings", u"1.1.1.1", None))
        self.label_7.setText(QCoreApplication.translate("dialog_settings", u"Database Port", None))
        self.input_dbport.setText(QCoreApplication.translate("dialog_settings", u"1234", None))
        self.label_10.setText(QCoreApplication.translate("dialog_settings", u"Other Settings", None))
        self.label_11.setText(QCoreApplication.translate("dialog_settings", u"Google Webhook", None))
        self.input_googlewebhook.setText(QCoreApplication.translate("dialog_settings", u"https://chat.googleapis.com/..", None))
        self.label_12.setText(QCoreApplication.translate("dialog_settings", u"Settings Path", None))
        self.input_settingspath.setText(QCoreApplication.translate("dialog_settings", u"P:/pipeline/standalone_dev/libs/credentials.json", None))
        self.label_13.setText(QCoreApplication.translate("dialog_settings", u"Omniverse Settings Path", None))
        self.input_omnisettings.setText(QCoreApplication.translate("dialog_settings", u"C:/some/path", None))
    # retranslateUi

    def load_settings(self):
        print("Loading settings")
        with open(self.input_settingspath.text(), "r") as f:
            settings = json.load(f)

        settings = {k: str(v) for k, v in settings.items()}

        self.input_serverip.setText(settings["server_ip"])
        self.input_serverport.setText(settings["server_port"])
        self.input_dbusrname.setText(settings["db_user"])
        self.input_dbpass.setText(settings["db_password"])
        self.input_dbname.setText(settings["db_name"])
        self.input_dbhost.setText(settings["db_host"])
        self.input_dbport.setText(settings["db_port"])
        self.input_googlewebhook.setText(settings["google_webhook_url"])
        print("Loaded settings")

    def save_settings(self):
        print("Saving settings")
        settings = dict()
        settings["server_ip"] = self.input_serverip.text()
        settings["server_port"] = self.input_serverport.text()
        settings["db_user"] = self.input_dbusrname.text()
        settings["db_password"] = self.input_dbpass.text()
        settings["db_name"] = self.input_dbname.text()
        settings["db_host"] = self.input_dbhost.text()
        settings["db_port"] = self.input_dbport.text()
        settings["google_webhook_url"] = self.input_googlewebhook.text()

        with open(self.input_settingspath.text(), "w") as f:
            json.dump(settings, f, indent=4)
        print("Saved settings")

    def close(self):
        print("Closing settings dialog")
        self.close()
