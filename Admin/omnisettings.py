from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

import json
class Ui_omniSettings(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(432, 354)
        self.horizontalLayoutWidget = QWidget(Form)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(9, 9, 421, 341))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.checkBox_rgb = QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_rgb.setObjectName(u"checkBox_rgb")
        self.checkBox_rgb.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_rgb)

        self.checkBox_normal = QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_normal.setObjectName(u"checkBox_normal")

        self.verticalLayout_2.addWidget(self.checkBox_normal)

        self.checkBox_bb2t = QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_bb2t.setObjectName(u"checkBox_bb2t")

        self.verticalLayout_2.addWidget(self.checkBox_bb2t)

        self.checkBox_bb2l = QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_bb2l.setObjectName(u"checkBox_bb2l")

        self.verticalLayout_2.addWidget(self.checkBox_bb2l)

        self.checkBox_bb3 = QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_bb3.setObjectName(u"checkBox_bb3")

        self.verticalLayout_2.addWidget(self.checkBox_bb3)

        self.checkBox_ss = QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_ss.setObjectName(u"checkBox_ss")

        self.verticalLayout_2.addWidget(self.checkBox_ss)

        self.checkBox_is = QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_is.setObjectName(u"checkBox_is")

        self.verticalLayout_2.addWidget(self.checkBox_is)

        self.checkBox_distcam = QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_distcam.setObjectName(u"checkBox_distcam")

        self.verticalLayout_2.addWidget(self.checkBox_distcam)

        self.checkBox_distplane = QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_distplane.setObjectName(u"checkBox_distplane")

        self.verticalLayout_2.addWidget(self.checkBox_distplane)

        self.checkBox_occ = QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_occ.setObjectName(u"checkBox_occ")

        self.verticalLayout_2.addWidget(self.checkBox_occ)

        self.checkBox_motvec = QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_motvec.setObjectName(u"checkBox_motvec")

        self.verticalLayout_2.addWidget(self.checkBox_motvec)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_2.addItem(self.horizontalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.input_savepath = QLineEdit(self.horizontalLayoutWidget)
        self.input_savepath.setObjectName(u"input_savepath")

        self.horizontalLayout_2.addWidget(self.input_savepath)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.comboBox_rendertype = QComboBox(self.horizontalLayoutWidget)
        self.comboBox_rendertype.addItem("")
        self.comboBox_rendertype.addItem("")
        self.comboBox_rendertype.setObjectName(u"comboBox_rendertype")

        self.horizontalLayout_3.addWidget(self.comboBox_rendertype)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.input_resw = QLineEdit(self.horizontalLayoutWidget)
        self.input_resw.setObjectName(u"input_resw")
        self.input_resw.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.input_resw)

        self.label_4 = QLabel(self.horizontalLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.input_resh = QLineEdit(self.horizontalLayoutWidget)
        self.input_resh.setObjectName(u"input_resh")
        self.input_resh.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.input_resh)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.button_save = QPushButton(self.horizontalLayoutWidget)
        self.button_save.setObjectName(u"button_save")

        self.verticalLayout.addWidget(self.button_save)

        self.button_close = QPushButton(self.horizontalLayoutWidget)
        self.button_close.setObjectName(u"button_close")

        self.verticalLayout.addWidget(self.button_close)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.checkBox_rgb.setText(QCoreApplication.translate("Form", u"RGB (png)", None))
        self.checkBox_normal.setText(QCoreApplication.translate("Form", u"Normal (png)", None))
        self.checkBox_bb2t.setText(QCoreApplication.translate("Form", u"BBox 2D tight", None))
        self.checkBox_bb2l.setText(QCoreApplication.translate("Form", u"BBox 2D loose", None))
        self.checkBox_bb3.setText(QCoreApplication.translate("Form", u"BBox 3D", None))
        self.checkBox_ss.setText(QCoreApplication.translate("Form", u"Semantic Segmentation", None))
        self.checkBox_is.setText(QCoreApplication.translate("Form", u"Instance Segmentation", None))
        self.checkBox_distcam.setText(QCoreApplication.translate("Form", u"Distance to Camera", None))
        self.checkBox_distplane.setText(QCoreApplication.translate("Form", u"Distance to Image Plane", None))
        self.checkBox_occ.setText(QCoreApplication.translate("Form", u"Occlusion", None))
        self.checkBox_motvec.setText(QCoreApplication.translate("Form", u"Motion Vectors", None))
        self.label.setText(QCoreApplication.translate("Form", u"Save Path", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Rendering", None))
        self.comboBox_rendertype.setItemText(0, QCoreApplication.translate("Form", u"RayTracedLighting", None))
        self.comboBox_rendertype.setItemText(1, QCoreApplication.translate("Form", u"PathTracing", None))

        self.label_3.setText(QCoreApplication.translate("Form", u"Resolution", None))
        self.input_resw.setText(QCoreApplication.translate("Form", u"1920", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"x", None))
        self.input_resh.setText(QCoreApplication.translate("Form", u"1080", None))
        self.button_save.setText(QCoreApplication.translate("Form", u"Save Settings", None))
        self.input_savepath.setText(QCoreApplication.translate("Form", u"P:\\pipeline\\standalone\\shared_settings.json", None))

        self.button_close.setText(QCoreApplication.translate("Form", u"Close w/o saving", None))
        self.button_close.clicked.connect(Form.close)
        self.button_save.clicked.connect(self.save_settings)
        self.load_settings()

    
    def load_settings(self):
        # try to load settings on open
        try :
            with open(self.input_savepath.text(), 'r') as f:
                settings = json.load(f)
                self.checkBox_rgb.setChecked(settings["rgb"])
                self.checkBox_normal.setChecked(settings["normal"])
                self.checkBox_bb2t.setChecked(settings["bb2t"])
                self.checkBox_bb2l.setChecked(settings["bb2l"])
                self.checkBox_bb3.setChecked(settings["bb3"])
                self.checkBox_ss.setChecked(settings["ss"])
                self.checkBox_is.setChecked(settings["is"])
                self.checkBox_distcam.setChecked(settings["distcam"])
                self.checkBox_distplane.setChecked(settings["distplane"])
                self.checkBox_occ.setChecked(settings["occ"])
                self.checkBox_motvec.setChecked(settings["motvec"])
                self.comboBox_rendertype.setCurrentText(settings["rendertype"])
                self.input_resw.setText(str(settings["resw"]))
                self.input_resh.setText(str(settings["resh"]))
        except Exception:
            pass
    
    def save_settings(self):
        path = self.input_savepath.text()
        print("Trying to save to: " + path)
        settings = {}
        for k, v in self.__dict__.items():
            if k.startswith("checkBox"):
                settings[k[9:]] = v.isChecked()
            elif k.startswith("input"):
                if k == "input_resw" or k == "input_resh":
                    settings[k[6:]] = int(v.text())
                else:
                    settings[k[6:]] = v.text()
            elif k.startswith("comboBox"):
                settings[k[9:]] = v.currentText()
        with open(path, "w") as f:
            json.dump(settings, f)