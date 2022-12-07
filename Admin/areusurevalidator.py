

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QPlainTextEdit, QPushButton, QSizePolicy, QWidget)

class Ui_areYouSureValid(object):
    def setupUi(self, areYouSure):
        if not areYouSure.objectName():
            areYouSure.setObjectName(u"areYouSure")
        areYouSure.resize(400, 184)
        self.horizontalLayoutWidget = QWidget(areYouSure)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(120, 130, 160, 51))
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
        self.plainTextEdit = QPlainTextEdit(areYouSure)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(120, 100, 161, 31))

        self.retranslateUi(areYouSure)

        self.areYouSure = areYouSure
        QMetaObject.connectSlotsByName(areYouSure)
    # setupUi
    
    def retranslateUi(self, areYouSure):
        areYouSure.setWindowTitle(QCoreApplication.translate("areYouSure", u"Sure ?", None))
        self.button_ok.setText(QCoreApplication.translate("areYouSure", u"OK", None))
        self.button_cancel.setText(QCoreApplication.translate("areYouSure", u"Cancel", None))
        self.text_question.setText(QCoreApplication.translate("areYouSure", u"Hi", None))
        self.areYouSure = areYouSure
        self.init_button_functions()


    def init_button_functions(self):
        self.button_ok.clicked.connect(self.check_validation)
        self.button_cancel.clicked.connect(self.areYouSure.close)
    
    def set_question(self, question, style=""):
        self.text_question.setText(question)
        self.text_question.setStyleSheet(style)
    
    def set_validation(self, validation):
        self.plainTextEdit.setPlaceholderText(validation)
        self.validation = validation
    
    def check_validation(self):
        if self.plainTextEdit.toPlainText().lower() == self.validation.lower():
            self.res = True
            self.areYouSure.close()
            print("Dogru")
        else:
            # Make the borders of plain text red
            self.res = False
            self.plainTextEdit.setStyleSheet("border: 1px solid red;")
        
        
    # retranslateUi

