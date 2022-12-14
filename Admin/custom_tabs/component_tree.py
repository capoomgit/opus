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

        self.addWidget(self.tree_view)
        # self.init_model()
        self.tree_view.clicked.connect(self.update_rhs)
        # Bind the deselect signal to something
        self.tree_view.selectionModel().selectionChanged.connect(self.deselect)


    def deselect(self, selected, deselected):
        # if all items are deselected, clear the parm settings
        if not self.tree_view.selectedIndexes():
            self.main.parm_settings.clear_model()

        if selected:
            self.update_rhs()

    def clear_layout(self, layout):
        """Recursively clear the layout of widgets and sublayouts"""
        for i in reversed(range(layout.count())):
            layout_item = layout.itemAt(i)
            if layout_item.widget() is not None:
                widget_to_remove = layout_item.widget()
                widget_to_remove.setParent(None)
                layout.removeWidget(widget_to_remove)

            elif layout_item.spacerItem() is not None:
                spacer_to_remove = layout_item.spacerItem()
                layout.removeItem(spacer_to_remove)

            else:
                layout_to_remove = layout.itemAt(i)
                self.clear_layout(layout_to_remove)

    # rhs = right hand side
    def update_rhs(self):
        # Get the selected item
        selected_item = self.tree_view.selectedIndexes()[0]
        selected_id = selected_item.siblingAtColumn(1).data()
        selected_type = selected_item.siblingAtColumn(2).data()
        self.clear_layout(self.main.parmLayout)
        # self.main.parm_settings.clear_model()
        # self.main.object_settings.clear_model()
        if selected_type == "Objects":
            self.update_object_settings(selected_item)
            # TODO: Add the object settings
        elif selected_type == "Components":
            pass
            # TODO: Add the component and path settings
        elif selected_type == "Paths":
            pass
            # TODO figure out if you want to do something if path is selected.
        elif selected_type == "Hdas":
            self.update_parm_settings(selected_item)


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
                for k, path in enumerate(paths):
                    parent_component.appendRow([StandardItem("Path #{}".format(k+1),align=Qt.AlignLeft),
                                                StandardItem(path["path_id"], align=Qt.AlignLeft),
                                                StandardItem("Paths", align=Qt.AlignLeft)])
                    hda_ids = path["hda_ids"]
                    parent_path = self.tree_model.item(i, 0).child(j, 0).child(k, 0)

                    self.db_cur.execute("""SELECT * FROM "Hdas" WHERE hda_id IN %s""", (tuple(hda_ids),))
                    hdas = self.db_cur.fetchall()

                    for hda in enumerate(hdas):
                        parent_path.appendRow([StandardItem(hda[1]["hda_name"].lower().replace(" ", ""),align=Qt.AlignLeft),
                                                    StandardItem(hda[1]["hda_id"], align=Qt.AlignLeft),
                                                    StandardItem("Hdas", align=Qt.AlignLeft)])

        self.tree_view.setModel(self.tree_model)

        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)

    # Delete all objects and children of those objects if any child doesn't containts the given string and highlight the text
    # TODO check if this breaks anything while a parm rule list is displayed
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
            self.tree_model.removeRows(to_remove - i, 1)


    def update_parm_settings(self, index : QModelIndex):
        # Get the item

        item = self.tree_model.itemFromIndex(index)

        # Get the table name from second column of the item
        table_name_index = index.sibling(item.row(), 2)
        table_name = self.tree_model.itemFromIndex(table_name_index).text()

        id_index = index.sibling(item.row(), 1)
        id = self.tree_model.itemFromIndex(id_index).text()


        self.main.parm_settings.init_model(id)

    def update_object_settings(self, index : QModelIndex):
        # item = self.tree_model.itemFromIndex(index)
        # id_index = index.sibling(item.row(), 1)
        # id = self.tree_model.itemFromIndex(id_index).text()

        self.main.object_settings.init_model()
        # self.main.object_settings.init_model(item)
    # Github copilot suggested this, we can maybe implement it later
    # def create_context_menu(self):
    #     self.context_menu = QMenu(self.tree_view)
    #     self.context_menu.addAction("Add HDA", self.add_hda)
    #     self.context_menu.addAction("Add Component", self.add_component)
    #     self.context_menu.addAction("Add Object", self.add_object)
    #     self.context_menu.addAction("Delete", self.delete)
    #     self.context_menu.addAction("Rename", self.rename)