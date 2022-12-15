from PySide6.QtWidgets import (QTreeView, QAbstractItemView,QHeaderView, QVBoxLayout, QMenu, QApplication, QWidget,
                               QScrollArea, QVBoxLayout, QLabel, QSlider, QLineEdit, QSpacerItem, QSizePolicy, QComboBox,
                               QPushButton)
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

            # Layout for parameters
            self.parm_layout = QVBoxLayout()

            self.scroll_widget = QWidget()
            self.scroll_widget.setLayout(self.parm_layout)
            self.scroll_widget.layout().setAlignment(Qt.AlignTop)

            self.scroll_area = QScrollArea()
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setWidget(self.scroll_widget)
            self.scroll_area.setFixedWidth(660)
            self.scroll_area.setFixedHeight(360)

            self.addWidget(self.scroll_area)


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
        self.hda_list_view.setFixedWidth(150)
        self.hda_list_view.setFixedHeight(130)

        # Set the selection mode to single selection
        self.hda_list_view.setSelectionMode(QAbstractItemView.SingleSelection)

        # Set the selection behavior to select rows
        self.hda_list_view.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Set the click event to create the parameter UI with the selected parameter id and index of the parameter
        self.hda_list_view.clicked.connect(lambda: self.create_parm_ui(db_parms[0]["parm_id"],
                                                                       self.hda_list_view.selectedIndexes()[0].row()))
        self.addWidget(self.hda_list_view)


    def create_parm_ui(self, parm_id, parm_index):
        """ This creates a UI for the selected parameter \n
            where you can change the min and max values and the default value"""

        # Clear the parameter layout
        for i in reversed(range(self.parm_layout.count())):
            self.parm_layout.itemAt(i).widget().setParent(None)


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

                parm_min_slider = QSlider(Qt.Horizontal)
                parm_max_slider = QSlider(Qt.Horizontal)

                parm_min_value_label = QLabel(str(db_parm["parm_min"][parm_index]))
                parm_max_value_label = QLabel(str(db_parm["parm_max"][parm_index]))

                self.parm_layout.addWidget(parm_name_label)
                self.parm_layout.addWidget(parm_min_label)
                self.parm_layout.addWidget(parm_min_slider)
                self.parm_layout.addWidget(parm_min_value_label)
                self.parm_layout.addWidget(parm_max_label)
                self.parm_layout.addWidget(parm_max_slider)
                self.parm_layout.addWidget(parm_max_value_label)

                # Connect the slider to the label
                parm_min_slider.valueChanged.connect(lambda: parm_min_value_label.setText(str(parm_min_slider.value())))
                parm_max_slider.valueChanged.connect(lambda: parm_max_value_label.setText(str(parm_max_slider.value())))

                # Add a spacer
                # self.parm_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))