from PySide6.QtWidgets import (QTreeView, QAbstractItemView,QHeaderView, QVBoxLayout, QHBoxLayout, QMenu, QApplication, QWidget,
                               QScrollArea, QVBoxLayout, QLabel, QSlider, QLineEdit, QSpacerItem, QSizePolicy, QComboBox,
                               QPushButton, QCheckBox, QFileDialog)
from PySide6.QtCore import (Qt, QRect, QModelIndex, QItemSelectionModel, QAbstractItemModel, QUrl)
from PySide6.QtGui import (QStandardItemModel, QStandardItem, QColor, QPalette, QBrush, QFont, QPainter, QKeySequence, QIntValidator)

import json, os
from collections import defaultdict

class CompView(QVBoxLayout):
    def __init__(self, db_conn, db_cur, main, parent=None):
        super(CompView, self).__init__(parent)

        self.db_cur = db_cur
        self.db_conn = db_conn
        self.main = main


    def init_model(self):
        pass