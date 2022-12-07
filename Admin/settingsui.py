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
 
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(150, 0))
 
        self.horizontalLayout_4.addWidget(self.label_3)
 
        self.input_libspath = QLineEdit(self.verticalLayoutWidget)
        self.input_libspath.setObjectName(u"input_libspath")
 
        self.horizontalLayout_4.addWidget(self.input_libspath)
 
 
        self.verticalLayout.addLayout(self.horizontalLayout_4)
 
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(150, 0))
 
        self.horizontalLayout_5.addWidget(self.label_4)
 
        self.input_hdapath = QLineEdit(self.verticalLayoutWidget)
        self.input_hdapath.setObjectName(u"input_hdapath")
 
        self.horizontalLayout_5.addWidget(self.input_hdapath)
 
 
        self.verticalLayout.addLayout(self.horizontalLayout_5)
 
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(150, 0))
 
        self.horizontalLayout_6.addWidget(self.label_5)
 
        self.input_settingspath = QLineEdit(self.verticalLayoutWidget)
        self.input_settingspath.setObjectName(u"input_settingspath")
 
        self.horizontalLayout_6.addWidget(self.input_settingspath)
 
 
        self.verticalLayout.addLayout(self.horizontalLayout_6)
 
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
 
        self.verticalLayout.addItem(self.verticalSpacer)
 
 
        self.retranslateUi(dialog_settings)
 
        QMetaObject.connectSlotsByName(dialog_settings)
    # setupUi
 
    def retranslateUi(self, dialog_settings):
        dialog_settings.setWindowTitle(QCoreApplication.translate("dialog_settings", u"Settings", None))
        self.button_save.setText(QCoreApplication.translate("dialog_settings", u"Save", None))
        self.button_close.setText(QCoreApplication.translate("dialog_settings", u"Close w/o saving", None))
        self.label_2.setText(QCoreApplication.translate("dialog_settings", u"Server IP", None))
        self.input_serverip.setText(QCoreApplication.translate("dialog_settings", u"192.168.168.130", None))
        self.label.setText(QCoreApplication.translate("dialog_settings", u"Server Port", None))
        self.input_serverport.setText(QCoreApplication.translate("dialog_settings", u"18812", None))
        self.label_3.setText(QCoreApplication.translate("dialog_settings", u"Libs Path", None))
        self.input_libspath.setText(QCoreApplication.translate("dialog_settings", u"P:\\pipeline\\standalone_dev\\libs", None))
        self.label_4.setText(QCoreApplication.translate("dialog_settings", u"HDA Save Path", None))
        self.input_hdapath.setText(QCoreApplication.translate("dialog_settings", u"P:\\pipeline\\standalone_dev\\saved", None))
        self.label_5.setText(QCoreApplication.translate("dialog_settings", u"Settings Save Path", None))
        self.input_settingspath.setText(QCoreApplication.translate("dialog_settings", u"P:\\pipeline\\standalone\\", None))
    # retranslateUi