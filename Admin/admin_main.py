from PySide6.QtCore import QTimer
import threading
import os, json, socket, configparser, time, uuid, gc

import psycopg2
import psycopg2.extras

from PySide6.QtCore import (QEvent)

from PySide6.QtGui import(
    QStandardItemModel, QStandardItem, QIntValidator
)

from PySide6.QtWidgets import(
    QDialog, QAbstractItemView
)

from admin import CapoomAdminClient
from settingsui import Ui_dialog_settings
from areusure import Ui_areYouSure
from areusurevalidator import Ui_areYouSureValid
from omnisettings import Ui_omniSettings

from consts import JobStatus, ClientStatus
from get_credentials import get_credentials
from custom_tabs.jobs_tab import JobView
from custom_tabs.component_tree import ComponentView
from custom_tabs.parm_settings_view import ParmView
from custom_tabs.obj_settings_view import ObjView


VERSION_PATH = "P:/pipeline/standalone/version.ini"
GET_JOB = """SELECT * FROM "Jobs" WHERE job_uuid = %s"""


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'adminclientskawVj.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
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
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QListView, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(1280, 720)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet(u"")
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
        self.verticalLayoutWidget.setGeometry(QRect(230, 10, 1041, 651))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"")
        self.commands = QWidget()
        self.commands.setObjectName(u"commands")
        self.verticalLayoutWidget_3 = QWidget(self.commands)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 20, 311, 591))
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

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_13 = QLabel(self.verticalLayoutWidget_3)
        self.label_13.setObjectName(u"label_13")
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_20.addWidget(self.label_13)

        self.input_version = QLineEdit(self.verticalLayoutWidget_3)
        self.input_version.setObjectName(u"input_version")

        self.horizontalLayout_20.addWidget(self.input_version)


        self.verticalLayout_4.addLayout(self.horizontalLayout_20)

        self.input_skipexist_cache = QCheckBox(self.verticalLayoutWidget_3)
        self.input_skipexist_cache.setObjectName(u"input_skipexist_cache")
        self.input_skipexist_cache.setChecked(True)

        self.verticalLayout_4.addWidget(self.input_skipexist_cache)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_prio = QLabel(self.verticalLayoutWidget_3)
        self.label_prio.setObjectName(u"label_prio")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_prio.sizePolicy().hasHeightForWidth())
        self.label_prio.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.label_prio)

        self.label_prioval = QLabel(self.verticalLayoutWidget_3)
        self.label_prioval.setObjectName(u"label_prioval")
        sizePolicy.setHeightForWidth(self.label_prioval.sizePolicy().hasHeightForWidth())
        self.label_prioval.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_prioval)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.slider_priority = QSlider(self.verticalLayoutWidget_3)
        self.slider_priority.setObjectName(u"slider_priority")
        self.slider_priority.setValue(50)
        self.slider_priority.setOrientation(Qt.Horizontal)

        self.verticalLayout_4.addWidget(self.slider_priority)

        self.line_5 = QFrame(self.verticalLayoutWidget_3)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.button_createhouse = QPushButton(self.verticalLayoutWidget_3)
        self.button_createhouse.setObjectName(u"button_createhouse")

        self.horizontalLayout_6.addWidget(self.button_createhouse)

        self.button_render = QPushButton(self.verticalLayoutWidget_3)
        self.button_render.setObjectName(u"button_render")

        self.horizontalLayout_6.addWidget(self.button_render)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.checkbox_startingstatus_cache = QCheckBox(self.verticalLayoutWidget_3)
        self.checkbox_startingstatus_cache.setObjectName(u"checkbox_startingstatus_cache")
        self.checkbox_startingstatus_cache.setChecked(True)

        self.verticalLayout_4.addWidget(self.checkbox_startingstatus_cache)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.button_cmd_loadtemplate = QPushButton(self.verticalLayoutWidget_3)
        self.button_cmd_loadtemplate.setObjectName(u"button_cmd_loadtemplate")

        self.horizontalLayout_9.addWidget(self.button_cmd_loadtemplate)

        self.input_template = QComboBox(self.verticalLayoutWidget_3)
        self.input_template.setObjectName(u"input_template")

        self.horizontalLayout_9.addWidget(self.input_template)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_structure = QLabel(self.verticalLayoutWidget_3)
        self.label_structure.setObjectName(u"label_structure")

        self.horizontalLayout_3.addWidget(self.label_structure)

        self.input_structure = QComboBox(self.verticalLayoutWidget_3)
        self.input_structure.setObjectName(u"input_structure")

        self.horizontalLayout_3.addWidget(self.input_structure)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.verticalLayoutWidget_4 = QWidget(self.commands)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(350, 20, 321, 591))
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

        self.input_skipexist_render = QCheckBox(self.verticalLayoutWidget_4)
        self.input_skipexist_render.setObjectName(u"input_skipexist_render")

        self.verticalLayout_5.addWidget(self.input_skipexist_render)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")

        self.verticalLayout_5.addLayout(self.horizontalLayout_18)

        self.button_omnisettings = QPushButton(self.verticalLayoutWidget_4)
        self.button_omnisettings.setObjectName(u"button_omnisettings")

        self.verticalLayout_5.addWidget(self.button_omnisettings)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.verticalLayoutWidget_5 = QWidget(self.commands)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(700, 20, 331, 591))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_14 = QLabel(self.verticalLayoutWidget_5)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_14)

        self.line_8 = QFrame(self.verticalLayoutWidget_5)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.HLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_8)

        self.input_stage_cache = QCheckBox(self.verticalLayoutWidget_5)
        self.input_stage_cache.setObjectName(u"input_stage_cache")
        self.input_stage_cache.setChecked(False)

        self.verticalLayout_3.addWidget(self.input_stage_cache)

        self.input_render_at_cache = QCheckBox(self.verticalLayoutWidget_5)
        self.input_render_at_cache.setObjectName(u"input_render_at_cache")
        self.input_render_at_cache.setChecked(False)

        self.verticalLayout_3.addWidget(self.input_render_at_cache)

        self.input_keepall = QCheckBox(self.verticalLayoutWidget_5)
        self.input_keepall.setObjectName(u"input_keepall")
        self.input_keepall.setChecked(True)

        self.verticalLayout_3.addWidget(self.input_keepall)

        self.label_3 = QLabel(self.verticalLayoutWidget_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.input_cache_hip = QCheckBox(self.verticalLayoutWidget_5)
        self.input_cache_hip.setObjectName(u"input_cache_hip")
        self.input_cache_hip.setChecked(False)

        self.horizontalLayout_2.addWidget(self.input_cache_hip)

        self.input_cache_usd = QCheckBox(self.verticalLayoutWidget_5)
        self.input_cache_usd.setObjectName(u"input_cache_usd")
        self.input_cache_usd.setChecked(True)

        self.horizontalLayout_2.addWidget(self.input_cache_usd)

        self.input_cache_bgeo = QCheckBox(self.verticalLayoutWidget_5)
        self.input_cache_bgeo.setObjectName(u"input_cache_bgeo")
        self.input_cache_bgeo.setChecked(True)

        self.horizontalLayout_2.addWidget(self.input_cache_bgeo)

        self.input_cache_glb = QCheckBox(self.verticalLayoutWidget_5)
        self.input_cache_glb.setObjectName(u"input_cache_glb")
        self.input_cache_glb.setChecked(False)

        self.horizontalLayout_2.addWidget(self.input_cache_glb)

        self.input_cache_gltf = QCheckBox(self.verticalLayoutWidget_5)
        self.input_cache_gltf.setObjectName(u"input_cache_gltf")
        self.input_cache_gltf.setChecked(False)

        self.horizontalLayout_2.addWidget(self.input_cache_gltf)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.label_5 = QLabel(self.verticalLayoutWidget_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_5)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.input_pointcloud = QCheckBox(self.verticalLayoutWidget_5)
        self.input_pointcloud.setObjectName(u"input_pointcloud")
        self.input_pointcloud.setChecked(False)

        self.horizontalLayout_19.addWidget(self.input_pointcloud)

        self.input_wireframe = QCheckBox(self.verticalLayoutWidget_5)
        self.input_wireframe.setObjectName(u"input_wireframe")
        self.input_wireframe.setChecked(False)

        self.horizontalLayout_19.addWidget(self.input_wireframe)


        self.verticalLayout_3.addLayout(self.horizontalLayout_19)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.tabWidget.addTab(self.commands, "")
        self.jobs = QWidget()
        self.jobs.setObjectName(u"jobs")
        self.horizontalLayoutWidget_5 = QWidget(self.jobs)
        self.horizontalLayoutWidget_5.setObjectName(u"horizontalLayoutWidget_5")
        self.horizontalLayoutWidget_5.setGeometry(QRect(10, 590, 1011, 31))
        self.horizontalLayout_12 = QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.button_start = QPushButton(self.horizontalLayoutWidget_5)
        self.button_start.setObjectName(u"button_start")

        self.horizontalLayout_12.addWidget(self.button_start)

        self.button_cancel = QPushButton(self.horizontalLayoutWidget_5)
        self.button_cancel.setObjectName(u"button_cancel")

        self.horizontalLayout_12.addWidget(self.button_cancel)

        self.button_pause = QPushButton(self.horizontalLayoutWidget_5)
        self.button_pause.setObjectName(u"button_pause")

        self.horizontalLayout_12.addWidget(self.button_pause)

        self.button_resume = QPushButton(self.horizontalLayoutWidget_5)
        self.button_resume.setObjectName(u"button_resume")

        self.horizontalLayout_12.addWidget(self.button_resume)

        self.button_updateworkers = QPushButton(self.horizontalLayoutWidget_5)
        self.button_updateworkers.setObjectName(u"button_updateworkers")

        self.horizontalLayout_12.addWidget(self.button_updateworkers)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer)

        self.checkbox_autorljobs = QCheckBox(self.horizontalLayoutWidget_5)
        self.checkbox_autorljobs.setObjectName(u"checkbox_autorljobs")

        self.horizontalLayout_12.addWidget(self.checkbox_autorljobs)

        self.button_refreshjobs = QPushButton(self.horizontalLayoutWidget_5)
        self.button_refreshjobs.setObjectName(u"button_refreshjobs")

        self.horizontalLayout_12.addWidget(self.button_refreshjobs)

        self.button_clearhistory = QPushButton(self.horizontalLayoutWidget_5)
        self.button_clearhistory.setObjectName(u"button_clearhistory")

        self.horizontalLayout_12.addWidget(self.button_clearhistory)

        self.verticalLayoutWidget_6 = QWidget(self.jobs)
        self.verticalLayoutWidget_6.setObjectName(u"verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(10, 10, 1021, 531))
        self.jobsLayout = QVBoxLayout(self.verticalLayoutWidget_6)
        self.jobsLayout.setObjectName(u"jobsLayout")
        self.jobsLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.jobsLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.jobs, "")
        self.hda_params = QWidget()
        self.hda_params.setObjectName(u"hda_params")
        self.verticalLayoutWidget_7 = QWidget(self.hda_params)
        self.verticalLayoutWidget_7.setObjectName(u"verticalLayoutWidget_7")
        self.verticalLayoutWidget_7.setGeometry(QRect(880, 530, 141, 91))
        self.verticalLayout_6 = QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.button_new_template = QPushButton(self.verticalLayoutWidget_7)
        self.button_new_template.setObjectName(u"button_new_template")

        self.verticalLayout_6.addWidget(self.button_new_template)

        self.button_load_template = QPushButton(self.verticalLayoutWidget_7)
        self.button_load_template.setObjectName(u"button_load_template")

        self.verticalLayout_6.addWidget(self.button_load_template)

        self.button_save_template = QPushButton(self.verticalLayoutWidget_7)
        self.button_save_template.setObjectName(u"button_save_template")
        self.button_save_template.setStyleSheet(u"font-weight:bold; color: green;")

        self.verticalLayout_6.addWidget(self.button_save_template)

        self.horizontalLayoutWidget_3 = QWidget(self.hda_params)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(10, 110, 311, 501))
        self.componentsLayout = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.componentsLayout.setObjectName(u"componentsLayout")
        self.componentsLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutWidget_4 = QWidget(self.hda_params)
        self.horizontalLayoutWidget_4.setObjectName(u"horizontalLayoutWidget_4")
        self.horizontalLayoutWidget_4.setGeometry(QRect(360, 40, 661, 491))
        self.parmLayout = QHBoxLayout(self.horizontalLayoutWidget_4)
        self.parmLayout.setObjectName(u"parmLayout")
        self.parmLayout.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.hda_params)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 10, 311, 20))
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_15 = QLabel(self.hda_params)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(360, 10, 661, 20))
        self.label_15.setAlignment(Qt.AlignCenter)
        self.line_2 = QFrame(self.hda_params)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(330, 30, 20, 581))
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.horizontalLayoutWidget_6 = QWidget(self.hda_params)
        self.horizontalLayoutWidget_6.setObjectName(u"horizontalLayoutWidget_6")
        self.horizontalLayoutWidget_6.setGeometry(QRect(10, 40, 311, 30))
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_structure_2 = QLabel(self.horizontalLayoutWidget_6)
        self.label_structure_2.setObjectName(u"label_structure_2")

        self.horizontalLayout_10.addWidget(self.label_structure_2)

        self.input_structure_2 = QComboBox(self.horizontalLayoutWidget_6)
        self.input_structure_2.setObjectName(u"input_structure_2")

        self.horizontalLayout_10.addWidget(self.input_structure_2)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_10)

        self.input_hda_search = QLineEdit(self.hda_params)
        self.input_hda_search.setObjectName(u"input_hda_search")
        self.input_hda_search.setGeometry(QRect(10, 80, 311, 21))
        self.input_hda_search.setAlignment(Qt.AlignCenter)
        self.tabWidget.addTab(self.hda_params, "")
        self.logs = QWidget()
        self.logs.setObjectName(u"logs")
        self.listView_logs = QListView(self.logs)
        self.listView_logs.setObjectName(u"listView_logs")
        self.listView_logs.setGeometry(QRect(10, 10, 1021, 601))
        self.tabWidget.addTab(self.logs, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 10, 211, 641))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")
        self.label.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
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
        self.button_select_avails = QPushButton(self.verticalLayoutWidget_2)
        self.button_select_avails.setObjectName(u"button_select_avails")

        self.horizontalLayout_5.addWidget(self.button_select_avails)

        self.button_select_all = QPushButton(self.verticalLayoutWidget_2)
        self.button_select_all.setObjectName(u"button_select_all")

        self.horizontalLayout_5.addWidget(self.button_select_all)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.list_clients = QListWidget(self.verticalLayoutWidget_2)
        self.list_clients.setObjectName(u"list_clients")

        self.verticalLayout_2.addWidget(self.list_clients)

        self.button_backupdb = QPushButton(self.verticalLayoutWidget_2)
        self.button_backupdb.setObjectName(u"button_backupdb")

        self.verticalLayout_2.addWidget(self.button_backupdb)

        self.button_connect = QPushButton(self.verticalLayoutWidget_2)
        self.button_connect.setObjectName(u"button_connect")

        self.verticalLayout_2.addWidget(self.button_connect)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.button_refresh = QPushButton(self.verticalLayoutWidget_2)
        self.button_refresh.setObjectName(u"button_refresh")

        self.horizontalLayout_8.addWidget(self.button_refresh)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.label_stat = QLabel(self.centralwidget)
        self.label_stat.setObjectName(u"label_stat")
        self.label_stat.setGeometry(QRect(10, 660, 1261, 21))
        self.label_stat.setAutoFillBackground(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1280, 22))
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
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Project Settings", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Project Id: ", None))
        self.input_projectid.setPlaceholderText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Count: ", None))
        self.input_count.setPlaceholderText("")
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Version:", None))
        self.input_version.setPlaceholderText("")
        self.input_skipexist_cache.setText(QCoreApplication.translate("MainWindow", u"Skip Existing Files - Cache", None))
        self.label_prio.setText(QCoreApplication.translate("MainWindow", u"Priority - ", None))
        self.label_prioval.setText(QCoreApplication.translate("MainWindow", u"50", None))
        self.button_createhouse.setText(QCoreApplication.translate("MainWindow", u"Cache Houses", None))
        self.button_render.setText(QCoreApplication.translate("MainWindow", u"Render Caches", None))
        self.checkbox_startingstatus_cache.setText(QCoreApplication.translate("MainWindow", u"Immidiately start the job", None))
        self.button_cmd_loadtemplate.setText(QCoreApplication.translate("MainWindow", u"Load Template", None))
        self.label_structure.setText(QCoreApplication.translate("MainWindow", u"Structure", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Render Settings", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Project Id: ", None))
        self.input_projectid_render.setPlaceholderText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Engine", None))
        self.input_engine.setItemText(0, QCoreApplication.translate("MainWindow", u"Omniverse", None))
        self.input_engine.setItemText(1, QCoreApplication.translate("MainWindow", u"Mantra", None))
        self.input_engine.setItemText(2, QCoreApplication.translate("MainWindow", u"Redshift", None))
        self.input_engine.setItemText(3, QCoreApplication.translate("MainWindow", u"Karma", None))

        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Type", None))
        self.input_type.setItemText(0, QCoreApplication.translate("MainWindow", u"360 Degree", None))
        self.input_type.setItemText(1, QCoreApplication.translate("MainWindow", u"Single Frame", None))

        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Frame Count", None))
        self.input_frame.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.input_frame.setPlaceholderText("")
        self.input_skipexist_render.setText(QCoreApplication.translate("MainWindow", u"Skip Existing Files - Render", None))
        self.button_omnisettings.setText(QCoreApplication.translate("MainWindow", u"Omniverse Render Settings", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Output Settings", None))
        self.input_stage_cache.setText(QCoreApplication.translate("MainWindow", u"Stage caches while creating", None))
        self.input_render_at_cache.setText(QCoreApplication.translate("MainWindow", u"Render While Creating", None))
        self.input_keepall.setText(QCoreApplication.translate("MainWindow", u"Keep all caches after merge", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"File Formats", None))
        self.input_cache_hip.setText(QCoreApplication.translate("MainWindow", u"hip", None))
        self.input_cache_usd.setText(QCoreApplication.translate("MainWindow", u"usd", None))
        self.input_cache_bgeo.setText(QCoreApplication.translate("MainWindow", u"bgeo.sc", None))
        self.input_cache_glb.setText(QCoreApplication.translate("MainWindow", u"glb", None))
        self.input_cache_gltf.setText(QCoreApplication.translate("MainWindow", u"gltf", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Synthetic Data", None))
        self.input_pointcloud.setText(QCoreApplication.translate("MainWindow", u"Point Cloud", None))
        self.input_wireframe.setText(QCoreApplication.translate("MainWindow", u"Wireframe", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.commands), QCoreApplication.translate("MainWindow", u"Commands", None))
        self.button_start.setText(QCoreApplication.translate("MainWindow", u"Start Job", None))
        self.button_cancel.setText(QCoreApplication.translate("MainWindow", u"Cancel Job", None))
        self.button_pause.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.button_resume.setText(QCoreApplication.translate("MainWindow", u"Resume", None))
        self.button_updateworkers.setText(QCoreApplication.translate("MainWindow", u"Update Workers", None))
        self.checkbox_autorljobs.setText(QCoreApplication.translate("MainWindow", u"Auto refresh", None))
        self.button_refreshjobs.setText(QCoreApplication.translate("MainWindow", u"Refresh Jobslist", None))
        self.button_clearhistory.setText(QCoreApplication.translate("MainWindow", u"Clear History", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.jobs), QCoreApplication.translate("MainWindow", u"Jobs", None))
        self.button_new_template.setText(QCoreApplication.translate("MainWindow", u"Create New Template", None))
        self.button_load_template.setText(QCoreApplication.translate("MainWindow", u"Load Template", None))
        self.button_save_template.setText(QCoreApplication.translate("MainWindow", u"Save Template", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Components and HDA's", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Parameter Randomization Interface", None))
        self.label_structure_2.setText(QCoreApplication.translate("MainWindow", u"Structure", None))
        self.input_hda_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search for Component or HDA", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.hda_params), QCoreApplication.translate("MainWindow", u"HDA setup", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.logs), QCoreApplication.translate("MainWindow", u"Logs", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Clients", None))
        self.button_select_avails.setText(QCoreApplication.translate("MainWindow", u"Sel. Availables", None))
        self.button_select_all.setText(QCoreApplication.translate("MainWindow", u"Force All", None))
        self.button_backupdb.setText(QCoreApplication.translate("MainWindow", u"Backup Database", None))
        self.button_connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.button_refresh.setText(QCoreApplication.translate("MainWindow", u"Refresh Client List", None))
        self.label_stat.setText(QCoreApplication.translate("MainWindow", u"Error", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


    def __init__(self, MainWindow):

        # Create an admin client
        self.admin = None
        self.adminthread = None
        self.omni_settings = {}
        self.refreshcd = 1000
        self.socket_name = socket.gethostname()


        self.mainWindow = MainWindow

        # Create the GUI
        self.setupUi(MainWindow)
        self.init_database()
        self.init_settings()
        self.init_omni_settings()
        self.init_jobs()
        self.init_components()
        self.init_parm_settings()
        self.init_object_settings()
        self.init_button_actions()
        self.init_client_list_view()
        self.init_structure_list()

        # Start the update timer
        self.timer = QTimer(self.mainWindow)
        self.timer.start(self.refreshcd)
        self.timer.timeout.connect(self.update)

        self.last_update_clients = []
        # Styles
        self.c_avail = QColor(196, 223, 170)
        self.c_busy = QColor(241, 202, 137)
        self.c_dnd = QColor(187, 100, 100)
        self.c_offline = QColor(100, 110, 120)

        self.template_path = None

    def init_button_actions(self):
        # Exit
        app.aboutToQuit.connect(self.exit)


        # Client list
        self.button_select_all.clicked.connect(self.select_all)
        self.button_select_avails.clicked.connect(self.select_avails)
        self.button_connect.clicked.connect(self.init_admin)
        self.button_refresh.clicked.connect(self.get_clients_from_server)
        self.button_backupdb.clicked.connect(self.backup_database)
        # Commands Tab
        self.button_createhouse.clicked.connect(self.create)
        self.button_render.clicked.connect(self.render)
        self.label_prioval.setText("50")
        self.slider_priority.valueChanged.connect(self.label_prioval.setNum)
        self.input_template.currentTextChanged.connect(self.update_template_path)
        # Commands Tab Validators
        self.input_projectid.setValidator(QIntValidator())
        self.input_frame.setValidator(QIntValidator())
        self.input_count.setValidator(QIntValidator())

        # self.button_stopall.clicked.connect(self.stop_all_jobs)
        self.button_cancel.clicked.connect(self.cancel_job)
        self.button_updateworkers.clicked.connect(self.send_new_workers)

        # Jobs Tab
        self.button_refreshjobs.clicked.connect(self.jobsview.refresh)
        self.button_clearhistory.clicked.connect(self.jobsview.clear_job_history)
        self.button_omnisettings.clicked.connect(self.open_omni_settings)
        self.button_pause.clicked.connect(self.pause_job)
        self.button_resume.clicked.connect(self.resume_job)

        self.button_cmd_loadtemplate.clicked.connect(self.load_template)

        # Settings Bar
        self.button_settings.triggered.connect(self.open_settings)
        self.button_updateclients.triggered.connect(self.update_clients)

        self.input_structure_2.currentTextChanged.connect(self.components.init_model)
        self.input_hda_search.textChanged.connect(self.components.search)

        # Parm Buttons

        self.button_load_template.clicked.connect(lambda: self.parm_settings.save_or_load_template(intent="load"))
        self.button_save_template.clicked.connect(lambda: self.parm_settings.save_or_load_template(intent="save"))
        self.button_new_template.clicked.connect(lambda: self.parm_settings.create_new_template())



    def init_database(self):
        credentials = get_credentials()
        dbname = credentials["db_name"]
        user = credentials["db_user"]
        password = credentials["db_password"]
        host = credentials["db_host"]
        port = credentials["db_port"]


        self.db_conn = psycopg2.connect(f"dbname={dbname} user={user} password={password} host={host}, port={port}")
        self.db_cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def init_settings(self):
        self.settingswidget = QDialog()

        self.settingsui=Ui_dialog_settings()
        self.settingsui.setupUi(self.settingswidget)
        self.settingsui.load_settings()
        self.settingsui.button_save.clicked.connect(self.settingsui.save_settings)
        self.settingsui.button_close.clicked.connect(self.settingsui.close)

    def init_omni_settings(self):
        self.omnisettingswidget = QDialog()
        self.omnisettingsui= Ui_omniSettings()
        self.omnisettingsui.setupUi(self.omnisettingswidget)

    def init_jobs(self):
        self.jobsview = JobView(self.db_conn, self.db_cur, self)
        self.jobsview.refresh()

        self.jobsLayout.addLayout(self.jobsview)
        self.jobsLayout.addLayout(self.horizontalLayout_12)

    def init_components(self):
        self.components = ComponentView(self.db_conn, self.db_cur, self)
        self.parmLayout.setAlignment(Qt.AlignTop)
        self.componentsLayout.addLayout(self.components)
        self.componentsLayout.addLayout(self.horizontalLayout_12)

    def init_parm_settings(self):
        self.parm_settings = ParmView(self.db_conn, self.db_cur, self)
        self.parmLayout.addLayout(self.parm_settings)

    def init_object_settings(self):
        self.object_settings = ObjView(self.db_conn, self.db_cur, self)
        self.parmLayout.addLayout(self.object_settings)

    def init_client_list_view(self):
        self.list_clients.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_clients.itemClicked.connect(self.cl_list_selection_behaviour)
        self.list_clients.setStyleSheet("QListWidget::indicator { width: 15px; height: 15px; }")

    def init_admin(self):
        self.admin = CapoomAdminClient(self.settingsui.input_serverip.text(), int(self.settingsui.input_serverport.text()))
        self.adminthread = threading.Thread(target=self.admin.run)
        self.adminthread.start()
        self.jobsview.refresh()
        
        # TODO hide the columns after setting model
        self.jobsview.refresh()

        self.admin_garbage_collector = threading.Thread(target=self.collect_garbage)
        self.admin_garbage_collector.start()


    def collect_garbage(self):
        while True:
            try:
                collected_objects = gc.collect()
                print(f"Garbage collector: collected {collected_objects} objects.")
            except Exception as e:
                print(e)
            time.sleep(300)
    
    def init_structure_list(self):
        self.input_structure.clear()
        self.input_structure_2.clear()

        self.db_cur.execute("""SELECT structure_name FROM "Structures" """)
        structures = self.db_cur.fetchall()

        for structure in structures:
            self.input_structure.addItem(structure[0])
            self.input_structure_2.addItem(structure[0])


    def cl_list_selection_behaviour(self):
        """ This function is called when the user clicks on a client in the list."""
        clicked_item = self.list_clients.currentItem()
        state_to_set = None
        if clicked_item.checkState() == Qt.Checked:
            state_to_set = Qt.Unchecked
        else:
            state_to_set = Qt.Checked

        for item in self.list_clients.selectedItems():
            item.setCheckState(state_to_set)


    def send_new_workers(self):
        new_workers = []
        for i in range(self.list_clients.count()):
            item = self.list_clients.item(i)
            # if item is selected then add it to the list
            if item.checkState() == Qt.Checked:
                new_workers.append(item.text())

        selected_jobs, jobinfo = self.jobsview.get_selected_jobs()
        self.admin.send_new_workers(new_workers, selected_jobs, jobinfo)

    def open_settings(self):
        self.settingswidget.exec()

    def open_omni_settings(self):

        # Try to load the settings
        try:
            with open(f"{self.settingsui.input_settingspath.text()}shared_settings.json") as f:
                self.omni_settings = json.load(f)
        except Exception as e:
            print("Couldn't load settings:", e)

        if self.omni_settings:
            self.omnisettingsui.load_settings()

        self.omnisettingswidget.exec()

    # THIS DOES NOT UPDATE THE JOBS WORKERS,
    # THIS UPDATES THE CLIENTS TO THE LATEST VERSION
    def update_clients(self):
        # Update the clients
        if self.admin is not None:
            rusurevalid = self.open_rusure_valid("Are you sure you want to update the clients?\nThis will stop all jobs and update the clients.", "Yes")
            if rusurevalid:
                self.admin.update_clients()

    def get_clients_from_server(self):
        if self.admin is not None:
            self.admin.get_clients_from_server()

    def update_status(self, running):
        if running:
            self.label_stat.setText("Status: Connected")
            self.label_stat.setStyleSheet("color: green")
        else:
            self.label_stat.setText("Error: Admin is not connected")
            self.label_stat.setStyleSheet("color: red")



    # This updates the client list if any client changes status/disconnects
    def update_client_list(self):

        selection = [item.text() for item in self.list_clients.selectedItems()]

        selected_jobs, _ = self.jobsview.get_selected_jobs()
        if len(selected_jobs) > 0 and self.jobs.isVisible():
            return

        if self.admin is not None:
            self.selected_workers = []

            for i in range(self.list_clients.count()):
                item = self.list_clients.item(i)
                # if item is selected then add it to the list
                if item.checkState() == Qt.Checked:
                    self.selected_workers.append(item.text())

            # No client changed
            if self.last_update_clients == self.admin.all_clients:
                return
            else:
                self.list_clients.clear()
                for client in self.admin.all_clients:
                    clientWidgetItem = QListWidgetItem(self.list_clients)
                    clientWidgetItem.setText(QCoreApplication.translate("MainWindow", client, None))
                    # clientWidgetItem.setText(client)

                    if client in self.selected_workers:
                        clientWidgetItem.setCheckState(Qt.Checked)
                    else:
                        clientWidgetItem.setCheckState(Qt.Unchecked)

                    if self.admin.all_clients[client] == ClientStatus.AVAILABLE.value:
                        clientWidgetItem.setForeground(self.c_avail)

                    elif self.admin.all_clients[client] == ClientStatus.BUSY.value:
                        clientWidgetItem.setForeground(self.c_busy)

                    elif self.admin.all_clients[client] == ClientStatus.DND.value:
                        clientWidgetItem.setForeground(self.c_dnd)

                    self.list_clients.addItem(clientWidgetItem)

                self.last_update_clients = self.admin.all_clients

            config = configparser.ConfigParser()
            config.read(VERSION_PATH)
            # Get all the keys of section IndividualUpdates
            all_updates = list(config['IndividualUpdates'].keys())
            all_updates = [str(x) for x in all_updates]

            cllist_from_admin = list(self.admin.all_clients.copy().keys())
            cllist_from_admin = [str(x) for x in cllist_from_admin]

            all_oflines = [all_updates.remove(x) for x in cllist_from_admin if x in all_updates]

            for client in all_updates:
                clientWidgetItem = QListWidgetItem(self.list_clients)
                clientWidgetItem.setText(QCoreApplication.translate("MainWindow", client, None))
                clientWidgetItem.setForeground(self.c_offline)
                clientWidgetItem.setCheckState(Qt.Unchecked)
                self.list_clients.addItem(clientWidgetItem)

            # Persist the selection
            for item in range(self.list_clients.count()):
                for sel in selection:
                    if self.list_clients.item(item).text() == sel:
                        self.list_clients.item(item).setSelected(True)

    def backup_database(self):
        if self.admin is not None:
            self.admin.backup_database()

    # This displays the jobs workers on the client list (by checking/unchecking the boxes)
    def selection_of_workers_for_job(self):
        selected_jobs, _ = self.jobsview.get_selected_jobs()

        if selected_jobs is not None and len(selected_jobs) > 0 and self.jobs.isVisible():
            self.job_workers = self.jobsview.get_selected_jobs_workers()
            self.job_workers = [x for x in self.job_workers if x is not None]

            for i in range(self.list_clients.count()):
                item = self.list_clients.item(i)
                if item.text() in self.job_workers:
                    item.setCheckState(Qt.Checked)
                else:
                    item.setCheckState(Qt.Unchecked)


    def create(self):

        if not self.omni_settings:
            try:
                with open(f"{self.settingsui.input_settingspath.text()}shared_settings.json") as f:
                    self.omni_settings = json.load(f)
            except Exception as e:
                self.omni_settings = self.omnisettingsui.load_settings()

        rusure = self.open_rusure(f"Are you sure you want to start a new job?\nProject ID:{self.input_projectid.text()} Count:{self.input_count.text()} Frame:{self.input_frame.text()}")
        if rusure:
            if self.admin is not None:

                # RENDER SETTINGS
                render_data = {}
                if self.input_render_at_cache.isChecked():
                    render_data["render"] = True
                    render_data["render_engine"] = self.input_engine.currentText().lower()

                    # get current index of self.i
                    if self.input_type.currentIndex() == 0:
                        render_data["frame_count"] = int(self.input_frame.text())
                else:
                    render_data["render"] = False

                # CACHE SETTINGS

                cache_data = {}
                cache_data["exports"] = []

                # BGEO
                if self.input_cache_bgeo.isChecked():
                    cache_data["exports"].append("bgeo.sc")

                # TODO HOUDINI DOESNT SUPPORT PATH/NAME ATTRIBUTES FOR HIERARCHY IN GLTF & GLB, WE NEED TO CHANGE THE WAY WE MERGE THE FILE FOR THIS
                # GLB
                if self.input_cache_glb.isChecked():
                    cache_data["exports"].append("glb")

                # GLTF
                if self.input_cache_gltf.isChecked():
                    cache_data["exports"].append("gltf")

                # USD
                if self.input_cache_usd.isChecked():
                    cache_data["exports"].append("usd")

                # HIP
                if self.input_cache_hip.isChecked():
                    cache_data["exports"].append("hip")

                if self.input_pointcloud.isChecked():
                    cache_data["exports"].append("pointcloud")
                
                if self.input_wireframe.isChecked():
                    cache_data["exports"].append("wireframe")
                    


                if self.input_keepall.isChecked():
                    cache_data["keepall"] = True


                all_data = {}
                # Omni settings
                try:
                    if render_data["render_engine"] == "omniverse":
                        all_data.update(self.omni_settings)
                except KeyError:
                    print("We are trying to set omni settings but we are not rendering at all")
                    pass

                all_data["projectid"] = int(self.input_projectid.text())
                all_data["skip"] = self.input_skipexist_cache.isChecked()
                all_data["version"] = self.input_version.text()

                all_data["structure"] = self.input_structure.currentText()

                all_data["stage"] = self.input_stage_cache.isChecked()

                if self.input_stage_cache.isChecked():
                    if self.input_frame.text() is None or self.input_frame.text() == "":
                        # TODO open dialog
                        print("Please enter a frame")
                        return
                    else:
                        all_data["frame_count"] = int(self.input_frame.text())

                all_data.update(render_data)
                all_data.update(cache_data)

                if self.template_path:
                    all_data.update({"template_path": self.template_path})
                else:
                    all_data.update({"template_path": ""})

                starting_state = None
                if self.checkbox_startingstatus_cache.isChecked():
                    starting_state = JobStatus.INPROGRESS.value
                else:
                    starting_state = JobStatus.NOTSTARTED.value
                self.admin.create_structure(self.get_selected_clients(self.list_clients),
                                        all_data,
                                        int(self.input_count.text()),
                                        self.input_version.text(),
                                        starting_state,
                                        self.socket_name,
                                        self.slider_priority.value())
    def render(self):
        all_data = {}
        if not self.omni_settings:
            try:
                with open(f"{self.settingsui.input_settingspath.text()}shared_settings.json") as f:
                    self.omni_settings = json.load(f)
                    print("Loaded settings:", self.omni_settings)
            except Exception as e:
                self.omni_settings = self.omnisettingsui.load_settings()
                print(e)

        render_job_count = len(self.input_renderuuid.text().split(","))
        rusure = self.open_rusure(f"Are you sure you want to start a rendering job\nJob Count:{render_job_count} Frame:{self.input_frame.text()} Engine:{self.input_engine.currentText()}")
        if rusure:
            if self.admin is not None:
                # RENDER SETTINGS
                render_data = {}
                render_data["render_engine"] = self.input_engine.currentText().lower()


                # get current index of self.i
                if self.input_type.currentIndex() == 0:
                    render_data["frame_count"] = int(self.input_frame.text())


                all_data = {}
                # Omni settings
                try:
                    if render_data["render_engine"] == "omniverse":
                        all_data.update(self.omni_settings)
                except KeyError:
                    print("Render engine not set")
                    pass


                # TODO Actually implement skip
                # all_data["skip"] = self.input_skipexist_render.isChecked()
                all_data["skip"] = False




                # Get this out of data
                all_data["projectid"] = 0

                all_data.update(render_data)

                cache_uuids = self.input_renderuuid.text().split(",")
                cache_uuids = [uuid.strip() for uuid in cache_uuids]
                print(cache_uuids)

                starting_state = None
                if self.checkbox_startingstatus_render.isChecked():
                    starting_state = JobStatus.INPROGRESS.value
                else:
                    starting_state = JobStatus.NOTSTARTED.value

                for cache_uuid in cache_uuids:
                    # TODO actually send the projectid
                    self.db_cur.execute(GET_JOB, (cache_uuid,))
                    actual_cache = self.db_cur.fetchone()
                    cache_count = int(actual_cache["count"])
                    cache_proj_id = int(actual_cache["project_id"])
                    structure = actual_cache["data"]["structure"]
                    print("Structure:", structure)

                    all_data["target_uuid"] = uuid.UUID(cache_uuid)
                    all_data["projectid"] = cache_proj_id
                    all_data["structure"] = structure
                    all_data["version"] = actual_cache["version"]

                    self.admin.render(self.get_selected_clients(self.list_clients),
                                            all_data,
                                            cache_count,
                                            self.input_version.text(),
                                            starting_state,
                                            self.socket_name,
                                            self.slider_priority.value())
                    time.sleep(1)

    def cancel_job(self):
        if self.admin is not None:
            jobuuids, jobinfos = self.jobsview.get_selected_jobs()
            self.admin.cancel_job(jobuuids, jobinfos)

            if not self.checkbox_autorljobs.isChecked():
                self.jobsview.refresh()

    def pause_job(self):
        if self.admin is not None:
            joblist, jobinfo = self.jobsview.get_selected_jobs()
            self.admin.pause_job(joblist, jobinfo)

            if not self.checkbox_autorljobs.isChecked():
                self.jobsview.refresh()

    def resume_job(self):
        if self.admin is not None:
            joblist, jobinfo = self.jobsview.get_selected_jobs()
            self.admin.resume_job(joblist, jobinfo)

        if not self.checkbox_autorljobs.isChecked():
            self.jobsview.refresh()

    def get_selected_clients(self, list):
        clients = []
        for i in range(list.count()):
            # get the widget
            item = list.item(i)
            # get the client name
            name = item.text()
            # check if it is selected
            if item.checkState() == Qt.Checked:
                clients.append(name)
        print("Selected clients: ", clients)
        return clients

    # Read from log file and write it to listView_logs
    def update_logs(self):
        # TODO get the path from setting
        if self.admin is not None:
            model = QStandardItemModel()
            self.listView_logs.setModel(model)
            with open(self.admin.logpath, "r") as f:
                for line in f:
                    item = QStandardItem(line)
                    model.appendRow(item)
            self.listView_logs.scrollToBottom()

    def select_all(self):
        rusure = self.open_rusure(f"Are you sure you want to select all workers?\nThis will override people that are offline")

        if rusure:
            for i in range(self.list_clients.count()):
                # get the widget
                item = self.list_clients.item(i)
                # get the client name
                if item.checkState() == Qt.Unchecked:
                    item.setCheckState(Qt.Checked)

    def select_avails(self):
        if self.admin is not None:

            # Look if we have check every available client already
            count = 0
            for i in range(self.list_clients.count()):
                item = self.list_clients.item(i)
                name = item.text()
                if name in self.admin.all_clients.keys():
                    if self.admin.all_clients[name] == ClientStatus.AVAILABLE.value and item.checkState() == Qt.Checked:
                        count += 1

            # Get all the available client count from admin.all_clients
            avail_count = 0
            for client in self.admin.all_clients.keys():
                if self.admin.all_clients[client] == ClientStatus.AVAILABLE.value:
                    avail_count += 1

            if count == avail_count:
                for i in range(self.list_clients.count()):
                    item = self.list_clients.item(i)
                    name = item.text()

                    if name in self.admin.all_clients.keys():
                        if self.admin.all_clients[name] == ClientStatus.AVAILABLE.value:
                            item.setCheckState(Qt.Unchecked)
            else:
                for i in range(self.list_clients.count()):
                    item = self.list_clients.item(i)
                    name = item.text()

                    if name in self.admin.all_clients.keys():
                        if self.admin.all_clients[name] == ClientStatus.AVAILABLE.value:
                            item.setCheckState(Qt.Checked)
    def open_rusure(self, question):
        rusurewidget = QDialog()
        rusureui = Ui_areYouSure()
        rusureui.setupUi(rusurewidget)
        rusureui.set_question(question)
        rusurewidget.exec()
        return rusureui.res

    def open_rusure_valid(self, question, validation):
        rusurewidget = QDialog()
        rusureui = Ui_areYouSureValid()
        rusureui.setupUi(rusurewidget)
        rusureui.set_question(question)
        rusureui.set_validation(validation)
        rusurewidget.exec()
        return rusureui.res

    def load_template(self):
        path = self.parm_settings.save_or_load_template("get_path")
        if path is not None:

            if self.input_template.findText(path) == -1:
                self.input_template.addItem(path)

            self.input_template.setCurrentText(path)
            self.template_path = path

    def update_template_path(self):
        self.template_path = self.input_template.currentText()

    def update(self):
        # Stuff that is visible from everywhere
        self.update_client_list()
        self.update_status(self.check_connection())


        if self.jobs.isVisible():
            if self.checkbox_autorljobs.isChecked():
                self.jobsview.refresh()

        if self.listView_logs.isVisible():
            self.update_logs()

    # Add exit function
    def exit(self):
        if self.admin is not None:
            self.admin.stop_connection()
        if self.adminthread is not None:
            print(self.adminthread.is_alive())
            self.adminthread = None
        sys.exit()

    def check_connection(self):
        if self.adminthread is not None and self.admin is not None:
            return self.admin.connected
        else:
            return False

if __name__ == "__main__":
    import sys
    # load qss
    darkstyle = open(f"P:\pipeline\standalone_dev\libs\darkstyle.qss", "r").read()

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    app.setWindowIcon(QIcon("P:/pipeline/standalone_dev/logo.png"))
    app.setStyleSheet(darkstyle)

    QFontDatabase.addApplicationFont('P:\\pipeline\\standalone_dev\\libs\\fonts\\Larsseit\\Larsseit-Bold.otf')
    app.setFont(QFont("Larsseit-Bold", 10))

    ui = Ui_MainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())