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

        self.tree_view.setRootIsDecorated(True)
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setModel(self.tree_model)
        self.addWidget(self.tree_view)

        self.init_model()
        self.tree_view.clicked.connect(self.update_model)

    def init_model(self):
        # Get the jobs
        self.db_cur.execute("""SELECT * FROM "Objects" """)
        objects = self.db_cur.fetchall()

        for i, object in enumerate(objects):
            self.tree_model.appendRow(StandardItem(object[1],
                                    #   set_color=QColor(255, 255, 255),
                                    #   set_background_color=QColor(0, 0, 0),
                                      align=Qt.AlignLeft))

            parent_object = self.tree_model.item(i, 0)

            component_ids = object["component_ids"]
            self.db_cur.execute("""SELECT * FROM "Components" WHERE component_id IN %s""", (tuple(component_ids),))
            components = self.db_cur.fetchall()

            for j, component in enumerate(components):

                parent_object.appendRow(StandardItem(component[1],
                                                    #  set_color=QColor(255, 255, 255),
                                                    #  set_background_color=QColor(0, 0, 0),
                                                     align=Qt.AlignLeft))

                parent_component = self.tree_model.item(i, 0).child(j, 0)

                path_ids = component["path_ids"]
                self.db_cur.execute("""SELECT * FROM "Paths" WHERE path_id IN %s""", (tuple(path_ids),))
                paths = self.db_cur.fetchall()

                for path in paths:
                    hda_ids = path["hda_ids"]

                    self.db_cur.execute("""SELECT * FROM "Hdas" WHERE hda_id IN %s""", (tuple(hda_ids),))
                    hdas = self.db_cur.fetchall()

                    for hda in enumerate(hdas):
                        parent_component.appendRow(StandardItem(hda[1]["hda_name"].lower().replace(" ", ""),
                                                #    set_color=QColor(255, 255, 255),
                                                #    set_background_color=QColor(0, 0, 0),
                                                   align=Qt.AlignLeft))

        self.tree_view.setModel(self.tree_model)

    def update_model(self, index):
        # TODO update the parameter interface
        print(index.row())
        pass
