# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'areusureHCITqz.ui'
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
    QPushButton, QSizePolicy, QWidget)

class Ui_areYouSure(object):
    def setupUi(self, areYouSure):
        if not areYouSure.objectName():
            areYouSure.setObjectName(u"areYouSure")
        areYouSure.resize(400, 150)
        self.horizontalLayoutWidget = QWidget(areYouSure)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(120, 90, 160, 51))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.button_ok = QPushButton(self.horizontalLayoutWidget)
        self.button_ok.setObjectName(u"button_ok")

        self.horizontalLayout.addWidget(self.button_ok)

        self.button_cancel = QPushButton(self.horizontalLayoutWidget)
        self.button_cancel.setObjectName(u"button_cancel")

        self.horizontalLayout.addWidget(self.button_cancel)

        self.text_question = QLabel(areYouSure)
        self.text_question.setObjectName(u"text_question")
        self.text_question.setGeometry(QRect(20, 20, 351, 41))
        self.text_question.setAlignment(Qt.AlignCenter)

        self.retranslateUi(areYouSure)

        QMetaObject.connectSlotsByName(areYouSure)
    # setupUi

    def retranslateUi(self, areYouSure):
        areYouSure.setWindowTitle(QCoreApplication.translate("areYouSure", u"Dialog", None))
        self.button_ok.setText(QCoreApplication.translate("areYouSure", u"OK", None))
        self.button_cancel.setText(QCoreApplication.translate("areYouSure", u"Cancel", None))
        self.text_question.setText(QCoreApplication.translate("areYouSure", u"Hi", None))
    # retranslateUi

