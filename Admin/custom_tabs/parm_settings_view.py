from PySide6.QtWidgets import (QTreeView, QAbstractItemView,QHeaderView, QVBoxLayout, QHBoxLayout, QMenu, QApplication, QWidget,
                               QScrollArea, QVBoxLayout, QLabel, QSlider, QLineEdit, QSpacerItem, QSizePolicy, QComboBox,
                               QPushButton, QCheckBox, QFileDialog)
from PySide6.QtCore import (Qt, QRect, QModelIndex, QItemSelectionModel, QAbstractItemModel, QUrl)
from PySide6.QtGui import (QStandardItemModel, QStandardItem, QColor, QPalette, QBrush, QFont, QPainter, QKeySequence, QIntValidator)

import json, os
from collections import defaultdict

# Create a widget that can be scrolled
class ParmView(QVBoxLayout):
    def __init__(self, db_conn, db_cur, main, parent=None):
        super(ParmView, self).__init__(parent)

        self.db_cur = db_cur
        self.db_conn = db_conn
        self.main = main

        # Layouts
        self.hda_version_layout = None
        self.hda_parms_list_view = None

        self.parm_layout = None
        self.parm_values_layout = None # Children of parm_layout
        self.parm_list_layout = None # Children of parm_layout

        self.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)
        self.selected_item = None
        # Declare new rules as a dictionary of dictionaries
        self.new_rules = defaultdict(dict)

        # Create a combobox
    def clear_model(self):
        # TODO There has to be a better way to do this
        try:
            self.hda_parms_list_view.setParent(None)
            self.hda_parms_list_view = None
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
            for i in reversed(range(self.parm_list_layout.count())):
                self.parm_layout.itemAt(i).widget().setParent(None)
        except Exception:
            pass

        try:
            for i in reversed(range(self.count())):
                self.itemAt(i).widget().setParent(None)
        except Exception:
            pass

        try:
            self.parm_random_rule_list.setParent(None)
        except Exception:
            pass




    def init_model(self, id, table_name):
        self.clear_model()

        if table_name == "Hdas":
            # Create the version layout
            self.hda_version_layout = QVBoxLayout()

            self.hda_version_layout.addWidget(QLabel("Selected Version:"))
            self.version_combobox = QComboBox()
            self.hda_version_layout.addWidget(self.version_combobox)

            self.update_used_version_button = QPushButton("Update Version")
            self.hda_version_layout.addWidget(self.update_used_version_button)

            self.addLayout(self.hda_version_layout)

            # Container layout
            self.parm_layout = QHBoxLayout()

            # Layout for parameter list
            self.parm_list_layout = QVBoxLayout()
            self.parm_list_layout.setAlignment(Qt.AlignTop)

            self.parm_layout.addLayout(self.parm_list_layout)
            # Fixed size for parm_layout
            # self.parm_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)

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
            self.version_combobox.addItems(hda_versions)
            self.initialize_parameter_list(id, hdas[0]["hda_version"])

    def initialize_parameter_list(self, hda_id, hda_version):
        """ This creates a list that shows all the parameters on the selected version of the HDA"""

        self.db_cur.execute("""SELECT * FROM "Parameters" WHERE hda_id = %s AND hda_version = %s""", (hda_id, hda_version))
        db_parms = self.db_cur.fetchall()

        self.hda_parms_list_view = QTreeView()
        self.hda_parms_list_model = QStandardItemModel()

        self.hda_parms_list_model.setHorizontalHeaderItem(0, QStandardItem("Parameter Name"))
        self.hda_parms_list_view.setModel(self.hda_parms_list_model)


        for db_parm in db_parms:
            for j in range(0, len(db_parm["parm_name"])):
                item = QStandardItem(db_parm["parm_name"][j])
                item.setEditable(False)
                self.hda_parms_list_model.appendRow(item)

        # Set fixed size
        self.hda_parms_list_view.setFixedWidth(200)
        self.hda_parms_list_view.setFixedHeight(130)
        self.init_parm_random_rule_list()
        self.hda_parms_list_view.clicked.connect(lambda: self.create_parm_ui(db_parms[0]["parm_id"], [x.row() for x in self.parm_random_rule_list.selectedIndexes()]))

        # Enable selection of multiple rows
        self.hda_parms_list_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Alternate row colors
        self.hda_parms_list_view.setAlternatingRowColors(True)

        # Set the alternate row colors
        self.hda_parms_list_view.setStyleSheet("alternate-background-color: rgb(30, 40, 50);")

        # Set minimum size
        self.hda_parms_list_view.setMinimumSize(150, 130)
        self.parm_list_layout.addWidget(self.hda_parms_list_view)



    def create_parm_ui(self, parm_id, sel_rule=None):
        """ This creates a UI for the selected parameter \n
            where you can change the min and max values and the default value"""

        sel_rows = self.hda_parms_list_view.selectionModel().selectedRows()
        sel_parm_indices = [sel_row.row() for sel_row in sel_rows]

        # Clear the parameter values layout
        for i in reversed(range(self.parm_values_layout.count())):
            if self.parm_values_layout.itemAt(i).widget() is not None:
                self.parm_values_layout.itemAt(i).widget().setParent(None)

        # Clear the spacer items
        for i in reversed(range(self.parm_values_layout.count())):
            if self.parm_values_layout.itemAt(i).spacerItem() is not None:
                self.parm_values_layout.removeItem(self.parm_values_layout.itemAt(i))
                i -= 1

        if sel_rule == None or len(sel_rule) == 0:
            self.db_cur.execute("""SELECT * FROM "Parameters" WHERE parm_id = %s""", (parm_id,))
            db_parms = self.db_cur.fetchall()

            if len(db_parms) == 0:
                # Display a message if there are no parameters
                return

            if len(db_parms) > 1:
                return

            # Visually, we just display the first selected index's values
            parm_min_value = db_parms[0]["parm_min"][sel_parm_indices[0]]
            parm_max_value = db_parms[0]["parm_max"][sel_parm_indices[0]]
            parm_default_value = db_parms[0]["parm_default"][sel_parm_indices[0]]
            parm_override_mode = db_parms[0]["parm_override"][sel_parm_indices[0]]
            parm_type = db_parms[0]["parm_type"][sel_parm_indices[0]]

            # parm names are the values of selected indices
            parm_names = []
            for sel_index in sel_parm_indices:
                parm_names.append(db_parms[0]["parm_name"][sel_index])

            weight = 100
        else:

            selected_item_index = self.main.components.tree_view.selectedIndexes()[0]

            selected_item_text = selected_item_index.data()
            selected_item_type = selected_item_index.siblingAtColumn(2).data()
            save_name = selected_item_type + "_" + selected_item_text

            # Get the parameter name
            parm_name = self.parm_random_rule_list.selectedIndexes()[0].parent().data()
            print("Parm name is",parm_name)

            print("Selected Item Text", selected_item_text)
            print("Selected Parm Name", parm_name)
            print("Selected Rule", sel_rule[0])


            # FIXME This should be a fucking sin
            # TODO Refactor the whole system to be in database or at least an ini file
            parm_min_value = self.new_rules[save_name][parm_name][sel_rule[0]][0][0]
            parm_max_value = self.new_rules[save_name][parm_name][sel_rule[0]][0][1]
            parm_default_value = self.new_rules[save_name][parm_name][sel_rule[0]][0][2]
            parm_override_mode = self.new_rules[save_name][parm_name][sel_rule[0]][0][3]
            parm_type = self.new_rules[save_name][parm_name][sel_rule[0]][0][4]

            weight = self.new_rules[save_name][parm_name][sel_rule[0]][1]
            parm_names = [parm_name]

        # Add a layout that contains the parameter name,
        # A slider for min and max values, and a text box for the current value
        parm_name_label = QLabel(", ".join(parm_names))
        parm_name_label.setAlignment(Qt.AlignCenter)
        # Make the parm name label multiline and wrap text
        parm_name_label.setWordWrap(True)
        # Give the inner text some spacing at the top and bottom while wrapping
        parm_name_label.setTextFormat(Qt.RichText)
        parm_name_label.setTextInteractionFlags(Qt.TextSelectableByMouse)


        parm_min_label = QLabel("Minimum")
        parm_max_label = QLabel("Maximum")
        parm_default_label = QLabel("Default")
        parm_override_mode_label = QLabel("Override Mode")
        parm_type_label = QLabel("Type")
        weight_label = QLabel("Weight")

        # Make the font size bigger in labels
        parm_name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        parm_min_label.setStyleSheet("font-size: 14px;")
        parm_max_label.setStyleSheet("font-size: 14px;")
        parm_default_label.setStyleSheet("font-size: 14px;")
        parm_override_mode_label.setStyleSheet("font-size: 14px;")
        parm_type_label.setStyleSheet("font-size: 14px;")
        weight_label.setStyleSheet("font-size: 14px;")


        parm_min_value_lineedit = QLineEdit(str(parm_min_value))
        parm_min_value_lineedit.setObjectName("parm_min_value_lineedit")

        parm_max_value_lineedit = QLineEdit(str(parm_max_value))
        parm_max_value_lineedit.setObjectName("parm_max_value_lineedit")

        parm_default_value_lineedit = QLineEdit(str(parm_default_value))
        parm_default_value_lineedit.setObjectName("parm_default_value_lineedit")

        parm_override_mode_combobox = QComboBox()
        parm_override_mode_combobox.addItems(["Random", "Default"])
        parm_override_mode_combobox.setObjectName("parm_override_mode_combobox")

        parm_override_mode_combobox.setCurrentIndex(parm_override_mode)

        parm_type_combobox = QComboBox()
        parm_type_combobox.setObjectName("parm_type_combobox")
        parm_type_combobox.addItems(["Float", "Int"])
        if parm_type == "Float":
            parm_type_combobox.setCurrentIndex(0)
        elif parm_type == "Int":
            parm_type_combobox.setCurrentIndex(1)

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
        self.parm_values_layout.addSpacerItem(QSpacerItem(0, spacing * 1.5, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.parm_values_layout.addWidget(weight_label)
        self.parm_values_layout.addSpacerItem(QSpacerItem(0, spacing, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.parm_weight_lineedit = QLineEdit(str(weight))
        self.parm_weight_lineedit.setFixedWidth(50)
        self.parm_weight_lineedit.setValidator(QIntValidator(1, 100))
        self.parm_weight_lineedit.setAlignment(Qt.AlignCenter)
        self.parm_weight_lineedit.setPlaceholderText("Weight")
        self.parm_weight_lineedit.setObjectName("parm_weight_lineedit")
        self.parm_values_layout.addWidget(self.parm_weight_lineedit)
        self.parm_values_layout.addSpacerItem(QSpacerItem(0, spacing, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.parm_add_rule_button = QPushButton("Add Rule")
        self.parm_add_rule_button.setFixedWidth(100)
        self.parm_add_rule_button.clicked.connect(self.add_parm_random_rule)
        self.parm_values_layout.addWidget(self.parm_add_rule_button)

    def init_parm_random_rule_list(self):
        """ Initializes a list of randomization rules of the loaded parameter template"""
        # TODO's:
        # create the new rule UI (add, weight etc)
        # show the rules in the list
        # use distinctive colors for the rules in the list
        # actually create the parameter template in the database or P:/pipeline
        # load the parameter template from the database or P:/pipeline
        # add the ability to edit the rules in the list
        # add the ability to delete the rules in the list

        self.parm_random_rule_list = QTreeView()
        self.parm_random_rule_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Create a model for the tree view
        parm_random_rule_list_model = QStandardItemModel()
        parm_random_rule_list_model.setHorizontalHeaderLabels(["Rule", "Weight"])
        self.parm_random_rule_list.setModel(parm_random_rule_list_model)

        self.parm_random_rule_list.clicked.connect(self.parm_random_rule_list_clicked)
        self.parm_random_rule_list.setFixedWidth(200)
        self.parm_random_rule_list.setFixedHeight(200)
        self.parm_random_rule_list.header().hide()


        # Add the list to the layout
        self.parm_list_layout.addWidget(self.parm_random_rule_list)

        # If new rules dict is not empty, refresh list
        if len(self.new_rules) != 0:
            self.refresh_random_rule_list()

    def parm_random_rule_list_clicked(self, index):
        """ Called when a rule in the random rule list is clicked """
        # Clear the parameter values layout
        for i in reversed(range(self.parm_values_layout.count())):
            if self.parm_values_layout.itemAt(i).widget() is not None:
                self.parm_values_layout.itemAt(i).widget().setParent(None)

        # Clear the spacer items
        for i in reversed(range(self.parm_values_layout.count())):
            if self.parm_values_layout.itemAt(i).spacerItem() is not None:
                self.parm_values_layout.removeItem(self.parm_values_layout.itemAt(i))
                i -= 1

        if self.hda_parms_list_view.selectionModel() != None:
            self.create_parm_ui(self.hda_parms_list_view.selectionModel().currentIndex(), [index.row()])

    def add_parm_random_rule(self):
        """ Adds a new randomization rule to the list """
        if self.hda_parms_list_view.selectionModel() != None:
            parm_names = self.hda_parms_list_view.selectionModel().selectedIndexes()
            parm_names = [self.hda_parms_list_view.model().itemFromIndex(parm_name).text() for parm_name in parm_names]


            # Create a new rule

            for parm_name in parm_names:

                # Add the new rule to the list
                selected_item_index = self.main.components.tree_view.selectedIndexes()[0]
                selected_item_text = selected_item_index.data()
                selected_item_type = selected_item_index.siblingAtColumn(2).data()
                save_name = selected_item_type + "_" + selected_item_text

                selected_version = self.version_combobox.currentText()
                # TODO: This is dangerous, fix it
                selected_version = float(selected_version)

                parm_values = []
                for i in range(self.parm_values_layout.count()):
                    # Get the line edits values
                    if self.parm_values_layout.itemAt(i).widget() is not None:
                        # Get the name of the widget
                        widget_name = self.parm_values_layout.itemAt(i).widget().objectName()

                        if widget_name == "parm_min_value_lineedit":
                            parm_values.append(self.parm_values_layout.itemAt(i).widget().text())

                        elif widget_name == "parm_max_value_lineedit":
                            parm_values.append(self.parm_values_layout.itemAt(i).widget().text())

                        elif widget_name == "parm_default_value_lineedit":
                            parm_values.append(self.parm_values_layout.itemAt(i).widget().text())

                        elif widget_name == "parm_override_mode_combobox":
                            parm_values.append(int(self.parm_values_layout.itemAt(i).widget().currentIndex()))

                        elif widget_name == "parm_type_combobox":
                            parm_values.append(self.parm_values_layout.itemAt(i).widget().currentText())

                        elif widget_name == "parm_weight_lineedit":
                            parm_weight = int(self.parm_values_layout.itemAt(i).widget().text())


                try:
                    if not isinstance(self.new_rules[save_name][parm_name], list):
                        self.new_rules[save_name][parm_name] = []
                except KeyError:
                    if save_name not in self.new_rules:
                        self.new_rules[save_name] = {}

                    if parm_name not in self.new_rules[save_name]:
                        self.new_rules[save_name][parm_name] = []

                self.new_rules[save_name + ".version"] = selected_version
                self.new_rules[save_name][parm_name].append([parm_values, parm_weight])

                print("New rule added to hda", save_name, "with parm", parm_name, "value", parm_values, "with weight", parm_weight)
            self.refresh_random_rule_list()


    def refresh_random_rule_list(self):
        """ Refreshes the random rule list """
        # Clear the model
        self.parm_random_rule_list.model().clear()




        selected_item_index = self.main.components.tree_view.selectedIndexes()[0]
        # Get the second column data of selected_item_index


        selected_item_text = selected_item_index.data()
        selected_item_type = selected_item_index.siblingAtColumn(2).data()
        save_name = selected_item_type + "_" + selected_item_text

        if save_name not in self.new_rules:
            return

        if save_name + ".version" not in self.new_rules:
            return

        # FIXME this needs to look at hda values not layer values, and it needs to save them like that as well
        parm_index = 0
        for parm in self.new_rules[save_name]:
            # TODO this is definitely not the best way to do this
            if parm == "version":
                continue

            print("Adding the parent parm", parm, "to the model")
            self.parm_random_rule_list.model().appendRow(QStandardItem(parm))
            # Get the last item in the model

            parent = self.parm_random_rule_list.model().item(parm_index)
            parm_index += 1
            for j, rule in enumerate(self.new_rules[save_name][parm], start=1):
                print("Adding the rule", rule, "to the parent", parent)
                # print("parm", parm, "rule", rule, "parmindex", parmindex, "j", j)
                # Get the parm item from the model

                parent.appendRow(QStandardItem("Rule {}".format(j)))

        self.version_combobox.setCurrentText(str(self.new_rules[save_name + ".version"]))

    def save_or_load_template(self, intent=None):
        new_file_dialog = QFileDialog()
        # Make the dialogue except only .json files
        new_file_dialog.setFileMode(QFileDialog.AnyFile)
        new_file_dialog.setNameFilter("JSON (*.json)")

        new_file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        new_file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)

        new_file_dialog.setSidebarUrls([QUrl.fromLocalFile("C:/"), QUrl.fromLocalFile("P:/"), QUrl.fromLocalFile("P:/pipeline/standalone/saved_templates")])
        new_file_dialog.setDirectory("P:/pipeline/standalone/saved_templates")

        if intent == "save":
            new_file_dialog.setAcceptMode(QFileDialog.AcceptSave)
            new_file_dialog.setLabelText(QFileDialog.Accept, "Save")

        elif intent == "load":
            new_file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
            new_file_dialog.setLabelText(QFileDialog.Accept, "Load")

        if new_file_dialog.exec():
            file_path = new_file_dialog.selectedFiles()[0]

            if intent == "save":
                self.save_template(file_path)

            elif intent == "load":
                self.load_template(file_path)

    def save_template(self, file_path):
        if not file_path.endswith(".json"):
            file_path += ".json"

        with open(file_path, "w") as f:
            json.dump(self.new_rules, f, indent=4)

    def load_template(self, file_path):
        # Check if the json contains the correct data
        if self.validate_template(file_path):
            with open(file_path, "r") as f:
                self.new_rules = json.load(f)

            print("Loaded template", file_path)

            # We reload just in case if the user has some parameter list open on the view
            try:
                self.refresh_random_rule_list()
            except Exception:
                pass

    def create_new_template(self):
        # TODO: check if the user has unsaved changes
        self.new_rules = {}
        self.refresh_random_rule_list()

    # This is 10x better to store in a database with seperate tables
    # TODO raise an error if the json is not valid with dialogue messages
    def validate_template(self, file_path):
        return True
        with open(file_path, "r") as f:
            data = json.load(f)

        for key, value in data.items():

            # Check if the key is either a component, a path or a hda in the database
            # if not self.main.components.tree_model.findItems(key):
                # print("Key is not a component or a path")
                # return False

            for parm, rules in value.items():
                print("parm", parm)
                print("rules", rules)
                # Check if the parm is in the database
                for rule in rules:
                    print("RULE IS", rule)
                    print("LEN IS ",len(rule))
                    # Check if the rule is a list
                    if not isinstance(rule, list):
                        print("Rule is not a list")
                        return False
                    # Check if the rule has a value and a weight
                    if len(rule) != 2:
                        print("Rule has not the correct amount of values")
                        return False

                    # Check if the rule value is a list
                    if not isinstance(rule[0], list):
                        print("Rule value is not a list")
                        return False

                    # Check if the rule value has the correct amount of values
                    if len(rule[0]) != 5:
                        print("Rule value has not the correct amount of values")
                        return False

                    # Check if the rule weight is an int
                    if not isinstance(rule[1], int):
                        print("Rule weight is not an int")
                        return False

        print("Template is valid")
        return True