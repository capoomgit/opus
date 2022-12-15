from PySide6.QtWidgets import (QTreeView, QAbstractItemView,QHeaderView, QVBoxLayout, QHBoxLayout, QMenu, QApplication, QWidget,
                               QScrollArea, QVBoxLayout, QLabel, QSlider, QLineEdit, QSpacerItem, QSizePolicy, QComboBox,
                               QPushButton, QCheckBox)
from PySide6.QtCore import (Qt, QRect, QModelIndex, QItemSelectionModel, QAbstractItemModel)
from PySide6.QtGui import (QStandardItemModel, QStandardItem, QColor, QPalette, QBrush, QFont, QPainter, QKeySequence)

# Create a widget that can be scrolled
class ParmView(QVBoxLayout):
    def __init__(self, db_conn, db_cur, main, parent=None):
        super(ParmView, self).__init__(parent)

        self.db_cur = db_cur
        self.db_conn = db_conn
        self.main = main



        # Layouts
        self.hda_version_layout = None
        self.hda_list_view = None

        self.parm_layout = None
        self.parm_values_layout = None # Children of parm_layout
        self.parm_list_layout = None # Children of parm_layout

        self.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)

        # Create a combobox
    def clear_model(self):

        try:
            self.hda_list_view.setParent(None)
            self.hda_list_view = None
        except Exception:
            pass

        try:
            for i in reversed(range(self.hda_version_layout.count())):
                self.hda_version_layout.itemAt(i).widget().setParent(None)
        except Exception:
            pass

        try:
            for i in reversed(range(self.parm_layout.count())):
                self.parm_layout.itemAt(i).widget().setParent(None)
        except Exception:
            pass

        try:
            for i in reversed(range(self.count())):
                self.itemAt(i).widget().setParent(None)
        except Exception:
            pass


    def init_model(self, id, table_name):
        self.clear_model()

        if table_name == "Hdas":
            # Create the version layout
            self.hda_version_layout = QVBoxLayout()

            self.hda_version_layout.addWidget(QLabel("Selected Version:"))
            self.combobox = QComboBox()
            self.hda_version_layout.addWidget(self.combobox)

            self.update_used_version_button = QPushButton("Update Version")
            self.hda_version_layout.addWidget(self.update_used_version_button)

            self.addLayout(self.hda_version_layout)

            # Container layout
            self.parm_layout = QHBoxLayout()

            # Layout for parameter list
            self.parm_list_layout = QVBoxLayout()
            self.parm_list_layout.setAlignment(Qt.AlignTop)

            self.parm_layout.addLayout(self.parm_list_layout)

            # Layout for parameters
            self.parm_values_layout = QVBoxLayout()

            self.scroll_widget = QWidget()
            self.scroll_widget.setLayout(self.parm_values_layout)
            self.scroll_widget.layout().setAlignment(Qt.AlignTop)

            self.scroll_area = QScrollArea()
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setWidget(self.scroll_widget)

            self.parm_values_layout.setAlignment(Qt.AlignTop)

            self.parm_layout.addWidget(self.scroll_area)

            self.addLayout(self.parm_layout)

            # This is a bit weird
            self.db_cur.execute("""SELECT * FROM "Hdas" WHERE hda_id = %s""", (id,))
            hda_name = self.db_cur.fetchone()["hda_name"]
            self.db_cur.execute("""SELECT * FROM "Hdas" WHERE hda_name = %s""", (hda_name,))
            hdas = self.db_cur.fetchall()
            hda_versions = [str(hda["hda_version"]) for hda in hdas]
            self.combobox.addItems(hda_versions)
            self.initialize_parameter_list(id, hdas[0]["hda_version"])

    def initialize_parameter_list(self, hda_id, hda_version):
        """ This creates a list that shows all the parameters on the selected version of the HDA"""


        self.db_cur.execute("""SELECT * FROM "Parameters" WHERE hda_id = %s AND hda_version = %s""", (hda_id, hda_version))
        db_parms = self.db_cur.fetchall()

        self.hda_list_view = QTreeView()
        self.hda_list_model = QStandardItemModel()

        self.hda_list_model.setHorizontalHeaderItem(0, QStandardItem("Parameter Name"))
        self.hda_list_view.setModel(self.hda_list_model)


        for db_parm in db_parms:
            for j in range(0, len(db_parm["parm_name"])):
                item = QStandardItem(db_parm["parm_name"][j])
                item.setEditable(False)
                self.hda_list_model.appendRow(item)

        # Set fixed size
        self.hda_list_view.setFixedWidth(200)
        self.hda_list_view.setFixedHeight(130)

        # Set the selection mode to single selection
        self.hda_list_view.setSelectionMode(QAbstractItemView.SingleSelection)

        # Set the selection behavior to select rows
        self.hda_list_view.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Set the click event to create the parameter UI with the selected parameter id and index of the parameter
        self.hda_list_view.clicked.connect(lambda: self.create_parm_ui(db_parms[0]["parm_id"],
                                                                       self.hda_list_view.selectedIndexes()[0].row()))

        # Alternate row colors
        self.hda_list_view.setAlternatingRowColors(True)

        # Set the alternate row colors
        self.hda_list_view.setStyleSheet("alternate-background-color: rgb(30, 40, 50);")

        # Set minimum size
        self.hda_list_view.setMinimumSize(150, 130)
        self.parm_list_layout.addWidget(self.hda_list_view)


    def create_parm_ui(self, parm_id, parm_index):
        """ This creates a UI for the selected parameter \n
            where you can change the min and max values and the default value"""

        # Clear the parameter values layout
        for i in reversed(range(self.parm_values_layout.count())):
            if self.parm_values_layout.itemAt(i).widget() is not None:
                self.parm_values_layout.itemAt(i).widget().setParent(None)

        # Clear the spacer items
        for i in reversed(range(self.parm_values_layout.count())):
            if self.parm_values_layout.itemAt(i).spacerItem() is not None:
                self.parm_values_layout.removeItem(self.parm_values_layout.itemAt(i))
                i -= 1

        self.db_cur.execute("""SELECT * FROM "Parameters" WHERE parm_id = %s""", (parm_id,))
        db_parms = self.db_cur.fetchall()

        if len(db_parms) > 1:
            # TODO add a warning dialog that says there are multiple parameters
            return

        if len(db_parms) == 0:
            # TODO add a warning dialog that says there are no parameters
            return


        # Add a layout that contains the parameter name,
        # A slider for min and max values, and a text box for the current value
        for i, db_parm in enumerate(db_parms):
                print(db_parm)
                parm_name_label = QLabel(db_parm["parm_name"][parm_index])
                parm_name_label.setAlignment(Qt.AlignCenter)

                parm_min_label = QLabel("Minimum")
                parm_max_label = QLabel("Maximum")
                parm_default_label = QLabel("Default")
                parm_override_mode_label = QLabel("Override Mode")
                parm_type_label = QLabel("Type")
                # Make the font size bigger in labels
                parm_min_label.setStyleSheet("font-size: 14px;")
                parm_max_label.setStyleSheet("font-size: 14px;")
                parm_default_label.setStyleSheet("font-size: 14px;")
                parm_override_mode_label.setStyleSheet("font-size: 14px;")
                parm_type_label.setStyleSheet("font-size: 14px;")
                parm_name_label.setStyleSheet("font-size: 16px; font-weight: bold;")


                parm_min_value_lineedit = QLineEdit(str(db_parm["parm_min"][parm_index]))
                parm_max_value_lineedit = QLineEdit(str(db_parm["parm_max"][parm_index]))
                parm_default_value_lineedit = QLineEdit(str(db_parm["parm_default"][parm_index]))

                parm_override_mode_combobox = QComboBox()
                parm_override_mode_combobox.addItems(["Random", "Default"])

                parm_type_combobox = QComboBox()
                parm_type_combobox.addItems(["Float", "Int"])

                spacing = 15
                self.parm_values_layout.addWidget(parm_name_label)
                self.parm_values_layout.addSpacerItem(QSpacerItem(0, spacing-spacing/3, QSizePolicy.Expanding, QSizePolicy.Minimum))

                self.parm_values_layout.addWidget(parm_min_label)
                self.parm_values_layout.addWidget(parm_min_value_lineedit)
                self.parm_values_layout.addSpacerItem(QSpacerItem(0, spacing, QSizePolicy.Expanding, QSizePolicy.Minimum))

                self.parm_values_layout.addWidget(parm_max_label)
                self.parm_values_layout.addWidget(parm_max_value_lineedit)
                self.parm_values_layout.addSpacerItem(QSpacerItem(0, spacing, QSizePolicy.Expanding, QSizePolicy.Minimum))

                self.parm_values_layout.addWidget(parm_default_label)
                self.parm_values_layout.addWidget(parm_default_value_lineedit)
                self.parm_values_layout.addSpacerItem(QSpacerItem(0, spacing, QSizePolicy.Expanding, QSizePolicy.Minimum))

                self.parm_values_layout.addWidget(parm_override_mode_label)
                self.parm_values_layout.addWidget(parm_override_mode_combobox)
                self.parm_values_layout.addSpacerItem(QSpacerItem(0, spacing, QSizePolicy.Expanding, QSizePolicy.Minimum))

                self.parm_values_layout.addWidget(parm_type_label)
                self.parm_values_layout.addWidget(parm_type_combobox)
                self.parm_values_layout.addSpacerItem(QSpacerItem(0, spacing, QSizePolicy.Expanding, QSizePolicy.Minimum))
