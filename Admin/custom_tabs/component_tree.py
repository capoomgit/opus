from PySide6.QtWidgets import (QTreeView, QAbstractItemView,QHeaderView, QVBoxLayout, QMenu, QApplication)
from PySide6.QtCore import (Qt, QRect, QModelIndex, QItemSelectionModel, QAbstractItemModel)
from PySide6.QtGui import (QStandardItemModel, QStandardItem, QColor, QPalette, QBrush, QFont, QPainter, QKeySequence)
from .ui_classes import TreeView, StandardItem

class ComponentView(QVBoxLayout):
    def __init__(self, db_conn, db_cur, main, parent=None):
        super(ComponentView, self).__init__(parent)

        self.tree_view = TreeView()

        # Create a model
        self.tree_model = QStandardItemModel()

        # self.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)
        # self.tree_view.setFixedWidth(240)
        # self.tree_view.setFixedHeight(500)
        # Get the jobs
        self.db_cur = db_cur
        self.db_conn = db_conn
        self.main = main

        self.tree_model.setHorizontalHeaderItem(0, QStandardItem("ITEM"))
        self.tree_model.setHorizontalHeaderItem(1, QStandardItem("ID"))
        self.tree_model.setHorizontalHeaderItem(2, QStandardItem("TABLE_NAME"))

        self.tree_view.setRootIsDecorated(True)
        self.tree_view.setHeaderHidden(True)

        self.tree_view.setModel(self.tree_model)

        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)

        print(self.tree_view.isColumnHidden(1))
        print(self.tree_view.isColumnHidden(2))

        self.addWidget(self.tree_view)
        # self.init_model()
        self.tree_view.clicked.connect(self.update_parm_settings)


    def init_model(self):
        # clear the model
        self.tree_model.clear()

        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)

        struct_name = self.main.input_structure_2.currentText()
        self.db_cur.execute("""SELECT * FROM "Structures" WHERE structure_name = %s""", (struct_name,))
        object_ids = self.db_cur.fetchone()["obj_ids"]
        self.db_cur.execute("""SELECT * FROM "Objects" WHERE obj_id IN %s""", (tuple(object_ids),))
        objects = self.db_cur.fetchall()

        for i, object in enumerate(objects):
            self.tree_model.appendRow([StandardItem(object[1], align=Qt.AlignLeft),
                                       StandardItem(object[0], align=Qt.AlignLeft),
                                       StandardItem("Objects", align=Qt.AlignLeft)])

            parent_object = self.tree_model.item(i, 0)

            component_ids = object["component_ids"]
            self.db_cur.execute("""SELECT * FROM "Components" WHERE component_id IN %s""", (tuple(component_ids),))
            components = self.db_cur.fetchall()

            for j, component in enumerate(components):

                parent_object.appendRow([StandardItem(component[1],align=Qt.AlignLeft),
                                         StandardItem(component[0], align=Qt.AlignLeft),
                                         StandardItem("Components", align=Qt.AlignLeft)])

                parent_component = self.tree_model.item(i, 0).child(j, 0)

                # TODO Add the path index to the tree, (i.e Path #1, Path #2, etc)
                # Maybe this will clutter since nearly all of our paths consists of only one hda?

                path_ids = component["path_ids"]
                self.db_cur.execute("""SELECT * FROM "Paths" WHERE path_id IN %s""", (tuple(path_ids),))
                paths = self.db_cur.fetchall()

                for path in paths:
                    hda_ids = path["hda_ids"]

                    self.db_cur.execute("""SELECT * FROM "Hdas" WHERE hda_id IN %s""", (tuple(hda_ids),))
                    hdas = self.db_cur.fetchall()

                    for hda in enumerate(hdas):
                        parent_component.appendRow([StandardItem(hda[1]["hda_name"].lower().replace(" ", ""),align=Qt.AlignLeft),
                                                    StandardItem(hda[1]["hda_id"], align=Qt.AlignLeft),
                                                    StandardItem("Hdas", align=Qt.AlignLeft)])

        self.tree_view.setModel(self.tree_model)

        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)

    # Delete all objects and children of those objects if any child doesn't containts the given string and highlight the text
    def search(self):
        text = self.main.input_hda_search.text()
        self.init_model()

        # FIXME This, for some reason doesnt search the inner children
        to_remove = []
        for i in range(self.tree_model.rowCount()):
            parent_object = self.tree_model.item(i, 0)
            found = False
            # Object contains the text
            if text.lower() in parent_object.text().lower():
                found = True

            for j in range(parent_object.rowCount()):
                parent_component = parent_object.child(j, 0)

                # Component contains the text
                if text.lower() in parent_component.text().lower():
                    found = True
                    break

                for k in range(parent_component.rowCount()):
                    parent_hda = parent_component.child(k, 0)

                    # HDA contains the text
                    if text.lower() in parent_hda.text().lower():
                        found = True
                        break
            if not found:
                to_remove.append(i)

        # Ew but it works
        for i, to_remove in enumerate(to_remove):
            print(self.tree_model.item(to_remove - i, 0).text())
            self.tree_model.removeRows(to_remove - i, 1)


    def update_parm_settings(self, index : QModelIndex):
        # Get the item

        # print("Index is ", index.row(), "!")
        item = self.tree_model.itemFromIndex(index)
        print("Item is ", item.text(), "!")

        # Get the table name from second column of the item
        table_name_index = index.sibling(item.row(), 2)
        table_name = self.tree_model.itemFromIndex(table_name_index).text()

        id_index = index.sibling(item.row(), 1)
        id = self.tree_model.itemFromIndex(id_index).text()

        self.main.parm_settings.init_model(id, table_name)


    # Github copilot suggested this, we can maybe implement it later
    # def create_context_menu(self):
    #     self.context_menu = QMenu(self.tree_view)
    #     self.context_menu.addAction("Add HDA", self.add_hda)
    #     self.context_menu.addAction("Add Component", self.add_component)
    #     self.context_menu.addAction("Add Object", self.add_object)
    #     self.context_menu.addAction("Delete", self.delete)
    #     self.context_menu.addAction("Rename", self.rename)