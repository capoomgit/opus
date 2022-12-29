from PySide6.QtWidgets import (QTreeView, QAbstractItemView,QHeaderView, QVBoxLayout, QHBoxLayout, QMenu, QApplication, QWidget,
                               QScrollArea, QVBoxLayout, QLabel, QSlider, QLineEdit, QSpacerItem, QSizePolicy, QComboBox,
                               QPushButton, QCheckBox, QFileDialog)
from PySide6.QtCore import (Qt, QRect, QModelIndex, QItemSelectionModel, QAbstractItemModel, QUrl)
from PySide6.QtGui import (QStandardItemModel, QStandardItem, QColor, QPalette, QBrush, QFont, QPainter, QKeySequence, QDoubleValidator)

import json, os
from collections import defaultdict

class ObjView(QVBoxLayout):
    def __init__(self, db_conn, db_cur, main, parent=None):
        super(ObjView, self).__init__(parent)

        self.db_cur = db_cur
        self.db_conn = db_conn
        self.main = main

        self.obj_settings_layout = None

    def clear_model(self):
        self.main.components.clear_layout(self.main.parmLayout)

    def init_model(self):
        self.clear_model()
        self.obj_settings_layout = QVBoxLayout()
        self.addLayout(self.obj_settings_layout)

        self.keep_at_cache_checkbox = QCheckBox()
        self.keep_at_cache_checkbox.setText("Keep at cache")

        self.can_skip_checkbox = QCheckBox()
        self.can_skip_checkbox.setText("Can skip")

        self.skip_chance_layout = QHBoxLayout()
        self.skip_chance_value_label = QLabel()
        self.skip_chance_value_label.setText("0.0")
        self.skip_chance_value_label.setFixedWidth(50)
        self.skip_chance_value_label.setFixedHeight(20)
        self.skip_chance_value_label.setAlignment(Qt.AlignRight)

        # QT doesnt support floats so we have to use a slider with a range of 0-100 and divide the value by 100 to get the float value
        self.skip_chance_slider = QSlider(Qt.Horizontal)
        self.skip_chance_slider.setMinimum(0)
        self.skip_chance_slider.setMaximum(100)
        self.skip_chance_slider.setValue(0)
        self.skip_chance_slider.valueChanged.connect(self.skip_chance_slider_value_changed)
        self.skip_chance_slider.setEnabled(False)

        self.skip_chance_layout.addWidget(self.skip_chance_value_label)
        self.skip_chance_layout.addWidget(self.skip_chance_slider)

        self.obj_settings_layout.addWidget(self.keep_at_cache_checkbox)
        self.obj_settings_layout.addWidget(self.can_skip_checkbox)
        self.obj_settings_layout.addLayout(self.skip_chance_layout)


        self.can_skip_checkbox.stateChanged.connect(self.can_skip_checkbox_state_changed)

    def can_skip_checkbox_state_changed(self):
        if self.can_skip_checkbox.isChecked():
            self.skip_chance_slider.setEnabled(True)
        else:
            self.skip_chance_slider.setEnabled(False)

    def skip_chance_slider_value_changed(self):
        self.skip_chance_value_label.setText(str(self.skip_chance_slider.value()/100))
