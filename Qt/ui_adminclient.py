# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'adminclientHjJEGU.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QListView,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(816, 615)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setIconSize(QSize(25, 50))
        MainWindow.setAnimated(True)
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.button_settings = QAction(MainWindow)
        self.button_settings.setObjectName(u"button_settings")
        self.button_updateclients = QAction(MainWindow)
        self.button_updateclients.setObjectName(u"button_updateclients")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(230, 10, 571, 531))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayoutWidget_3 = QWidget(self.tab)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 30, 255, 371))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.verticalLayoutWidget_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_7)

        self.line_3 = QFrame(self.verticalLayoutWidget_3)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_2 = QLabel(self.verticalLayoutWidget_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_7.addWidget(self.label_2)

        self.input_projectid = QLineEdit(self.verticalLayoutWidget_3)
        self.input_projectid.setObjectName(u"input_projectid")
        self.input_projectid.setClearButtonEnabled(False)

        self.horizontalLayout_7.addWidget(self.input_projectid)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_6 = QLabel(self.verticalLayoutWidget_3)
        self.label_6.setObjectName(u"label_6")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_11.addWidget(self.label_6)

        self.input_count = QLineEdit(self.verticalLayoutWidget_3)
        self.input_count.setObjectName(u"input_count")

        self.horizontalLayout_11.addWidget(self.input_count)


        self.verticalLayout_4.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.input_skipexist_cache = QCheckBox(self.verticalLayoutWidget_3)
        self.input_skipexist_cache.setObjectName(u"input_skipexist_cache")
        self.input_skipexist_cache.setChecked(True)

        self.horizontalLayout_17.addWidget(self.input_skipexist_cache)


        self.verticalLayout_4.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.input_render_at_cache = QCheckBox(self.verticalLayoutWidget_3)
        self.input_render_at_cache.setObjectName(u"input_render_at_cache")
        self.input_render_at_cache.setChecked(True)

        self.horizontalLayout_19.addWidget(self.input_render_at_cache)


        self.verticalLayout_4.addLayout(self.horizontalLayout_19)

        self.input_keepall = QCheckBox(self.verticalLayoutWidget_3)
        self.input_keepall.setObjectName(u"input_keepall")
        self.input_keepall.setChecked(True)

        self.verticalLayout_4.addWidget(self.input_keepall)

        self.line_5 = QFrame(self.verticalLayoutWidget_3)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_5)

        self.label_3 = QLabel(self.verticalLayoutWidget_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_3)

        self.line_6 = QFrame(self.verticalLayoutWidget_3)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.input_cache_hip = QCheckBox(self.verticalLayoutWidget_3)
        self.input_cache_hip.setObjectName(u"input_cache_hip")
        self.input_cache_hip.setChecked(False)

        self.horizontalLayout_2.addWidget(self.input_cache_hip)

        self.input_cache_usd = QCheckBox(self.verticalLayoutWidget_3)
        self.input_cache_usd.setObjectName(u"input_cache_usd")
        self.input_cache_usd.setChecked(True)

        self.horizontalLayout_2.addWidget(self.input_cache_usd)

        self.input_cache_bgeo = QCheckBox(self.verticalLayoutWidget_3)
        self.input_cache_bgeo.setObjectName(u"input_cache_bgeo")
        self.input_cache_bgeo.setChecked(True)

        self.horizontalLayout_2.addWidget(self.input_cache_bgeo)

        self.input_cache_glb = QCheckBox(self.verticalLayoutWidget_3)
        self.input_cache_glb.setObjectName(u"input_cache_glb")
        self.input_cache_glb.setChecked(False)

        self.horizontalLayout_2.addWidget(self.input_cache_glb)

        self.input_cache_gltf = QCheckBox(self.verticalLayoutWidget_3)
        self.input_cache_gltf.setObjectName(u"input_cache_gltf")
        self.input_cache_gltf.setChecked(False)

        self.horizontalLayout_2.addWidget(self.input_cache_gltf)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.horizontalLayoutWidget_2 = QWidget(self.tab)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 410, 251, 80))
        self.horizontalLayout_6 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.button_createhouse = QPushButton(self.horizontalLayoutWidget_2)
        self.button_createhouse.setObjectName(u"button_createhouse")

        self.horizontalLayout_6.addWidget(self.button_createhouse)

        self.button_render = QPushButton(self.horizontalLayoutWidget_2)
        self.button_render.setObjectName(u"button_render")

        self.horizontalLayout_6.addWidget(self.button_render)

        self.verticalLayoutWidget_4 = QWidget(self.tab)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(290, 30, 260, 371))
        self.verticalLayout_5 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.verticalLayoutWidget_4)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_8)

        self.line_4 = QFrame(self.verticalLayoutWidget_4)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_5.addWidget(self.line_4)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_9 = QLabel(self.verticalLayoutWidget_4)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_13.addWidget(self.label_9)

        self.input_projectid_render = QLineEdit(self.verticalLayoutWidget_4)
        self.input_projectid_render.setObjectName(u"input_projectid_render")
        self.input_projectid_render.setClearButtonEnabled(False)

        self.horizontalLayout_13.addWidget(self.input_projectid_render)


        self.verticalLayout_5.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_11 = QLabel(self.verticalLayoutWidget_4)
        self.label_11.setObjectName(u"label_11")
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_15.addWidget(self.label_11)

        self.input_engine = QComboBox(self.verticalLayoutWidget_4)
        self.input_engine.addItem("")
        self.input_engine.addItem("")
        self.input_engine.addItem("")
        self.input_engine.setObjectName(u"input_engine")
        self.input_engine.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_15.addWidget(self.input_engine)


        self.verticalLayout_5.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_12 = QLabel(self.verticalLayoutWidget_4)
        self.label_12.setObjectName(u"label_12")
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_16.addWidget(self.label_12)

        self.input_type = QComboBox(self.verticalLayoutWidget_4)
        self.input_type.addItem("")
        self.input_type.addItem("")
        self.input_type.setObjectName(u"input_type")
        self.input_type.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_16.addWidget(self.input_type)


        self.verticalLayout_5.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_10 = QLabel(self.verticalLayoutWidget_4)
        self.label_10.setObjectName(u"label_10")
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_14.addWidget(self.label_10)

        self.input_frame = QLineEdit(self.verticalLayoutWidget_4)
        self.input_frame.setObjectName(u"input_frame")

        self.horizontalLayout_14.addWidget(self.input_frame)


        self.verticalLayout_5.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.input_skipexist_render = QCheckBox(self.verticalLayoutWidget_4)
        self.input_skipexist_render.setObjectName(u"input_skipexist_render")

        self.horizontalLayout_18.addWidget(self.input_skipexist_render)


        self.verticalLayout_5.addLayout(self.horizontalLayout_18)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.line_2 = QFrame(self.tab)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(270, 30, 20, 361))
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayoutWidget_5 = QWidget(self.tab_2)
        self.horizontalLayoutWidget_5.setObjectName(u"horizontalLayoutWidget_5")
        self.horizontalLayoutWidget_5.setGeometry(QRect(150, 470, 241, 31))
        self.horizontalLayout_12 = QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.button_stop = QPushButton(self.horizontalLayoutWidget_5)
        self.button_stop.setObjectName(u"button_stop")

        self.horizontalLayout_12.addWidget(self.button_stop)

        self.button_stopall = QPushButton(self.horizontalLayoutWidget_5)
        self.button_stopall.setObjectName(u"button_stopall")
        font = QFont()
        font.setBold(True)
        font.setUnderline(False)
        self.button_stopall.setFont(font)
        icon = QIcon()
        iconThemeName = u"view-refresh"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.button_stopall.setIcon(icon)

        self.horizontalLayout_12.addWidget(self.button_stopall)

        self.listWidget_Jobs = QListWidget(self.tab_2)
        self.listWidget_Jobs.setObjectName(u"listWidget_Jobs")
        self.listWidget_Jobs.setGeometry(QRect(10, 10, 541, 441))
        self.tabWidget.addTab(self.tab_2, "")
        self.logs = QWidget()
        self.logs.setObjectName(u"logs")
        self.listView_logs = QListView(self.logs)
        self.listView_logs.setObjectName(u"listView_logs")
        self.listView_logs.setGeometry(QRect(10, 10, 541, 491))
        self.tabWidget.addTab(self.logs, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 10, 211, 531))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")
        self.label.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(0, 16))
        self.label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label)

        self.line = QFrame(self.verticalLayoutWidget_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.button_select_all = QPushButton(self.verticalLayoutWidget_2)
        self.button_select_all.setObjectName(u"button_select_all")

        self.horizontalLayout_5.addWidget(self.button_select_all)

        self.button_select_avails = QPushButton(self.verticalLayoutWidget_2)
        self.button_select_avails.setObjectName(u"button_select_avails")

        self.horizontalLayout_5.addWidget(self.button_select_avails)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.listWidget = QListWidget(self.verticalLayoutWidget_2)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout_2.addWidget(self.listWidget)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.button_refresh = QPushButton(self.verticalLayoutWidget_2)
        self.button_refresh.setObjectName(u"button_refresh")

        self.horizontalLayout_8.addWidget(self.button_refresh)

        self.button_updateworkers = QPushButton(self.verticalLayoutWidget_2)
        self.button_updateworkers.setObjectName(u"button_updateworkers")

        self.horizontalLayout_8.addWidget(self.button_updateworkers)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.input_autoassign = QCheckBox(self.verticalLayoutWidget_2)
        self.input_autoassign.setObjectName(u"input_autoassign")
        self.input_autoassign.setChecked(True)

        self.verticalLayout_2.addWidget(self.input_autoassign)

        self.label_stat = QLabel(self.centralwidget)
        self.label_stat.setObjectName(u"label_stat")
        self.label_stat.setGeometry(QRect(10, 550, 681, 21))
        self.label_stat.setAutoFillBackground(True)
        self.button_connect = QPushButton(self.centralwidget)
        self.button_connect.setObjectName(u"button_connect")
        self.button_connect.setGeometry(QRect(720, 550, 75, 24))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 816, 22))
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuSettings.menuAction())
        self.menuSettings.addAction(self.button_settings)
        self.menuSettings.addAction(self.button_updateclients)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Capoom Admin", None))
        self.button_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.button_updateclients.setText(QCoreApplication.translate("MainWindow", u"!Update Clients!", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"House Create Settings", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Project Id: ", None))
        self.input_projectid.setPlaceholderText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Count: ", None))
        self.input_count.setPlaceholderText("")
        self.input_skipexist_cache.setText(QCoreApplication.translate("MainWindow", u"Skip Existing Files", None))
        self.input_render_at_cache.setText(QCoreApplication.translate("MainWindow", u"Render While Creating", None))
        self.input_keepall.setText(QCoreApplication.translate("MainWindow", u"Keep all caches after merge", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"File Formats", None))
        self.input_cache_hip.setText(QCoreApplication.translate("MainWindow", u"hip", None))
        self.input_cache_usd.setText(QCoreApplication.translate("MainWindow", u"usd", None))
        self.input_cache_bgeo.setText(QCoreApplication.translate("MainWindow", u"bgeo.sc", None))
        self.input_cache_glb.setText(QCoreApplication.translate("MainWindow", u"glb", None))
        self.input_cache_gltf.setText(QCoreApplication.translate("MainWindow", u"gltf", None))
        self.button_createhouse.setText(QCoreApplication.translate("MainWindow", u"Cache Houses", None))
        self.button_render.setText(QCoreApplication.translate("MainWindow", u"Render Caches", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Render Settings", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Project Id: ", None))
        self.input_projectid_render.setPlaceholderText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Engine", None))
        self.input_engine.setItemText(0, QCoreApplication.translate("MainWindow", u"Redshift", None))
        self.input_engine.setItemText(1, QCoreApplication.translate("MainWindow", u"Mantra", None))
        self.input_engine.setItemText(2, QCoreApplication.translate("MainWindow", u"Omniverse", None))

        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Type", None))
        self.input_type.setItemText(0, QCoreApplication.translate("MainWindow", u"360 Degree", None))
        self.input_type.setItemText(1, QCoreApplication.translate("MainWindow", u"Single Frame", None))

        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Frame Count", None))
        self.input_frame.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.input_frame.setPlaceholderText("")
        self.input_skipexist_render.setText(QCoreApplication.translate("MainWindow", u"Skip Existing Files", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Commands", None))
        self.button_stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.button_stopall.setText(QCoreApplication.translate("MainWindow", u"Stop All", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Jobs", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.logs), QCoreApplication.translate("MainWindow", u"Logs", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Clients", None))
        self.button_select_all.setText(QCoreApplication.translate("MainWindow", u"Select All", None))
        self.button_select_avails.setText(QCoreApplication.translate("MainWindow", u"Select Avails", None))
        self.button_refresh.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.button_updateworkers.setText(QCoreApplication.translate("MainWindow", u"Update Workers", None))
        self.input_autoassign.setText(QCoreApplication.translate("MainWindow", u"Automatically assign new clients", None))
        self.label_stat.setText(QCoreApplication.translate("MainWindow", u"Error", None))
        self.button_connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

