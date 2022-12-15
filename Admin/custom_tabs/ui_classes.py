from PySide6.QtWidgets import (QTreeView, QAbstractItemView, QHeaderView)
from PySide6.QtGui import (QStandardItem, QBrush, QColor, QFont, QPalette)
from PySide6.QtCore import (Qt)


class TreeView(QTreeView):
    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setUniformRowHeights(True)
        self.setAllColumnsShowFocus(True)
        self.setWordWrap(True)
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.header().setStyleSheet("QHeaderView::section {min-width: 28ex;}")
        self.header().setStretchLastSection(False)
        self.header().setSortIndicatorShown(True)
        self.header().setSortIndicator(0, Qt.SortOrder.AscendingOrder)
        self.header().setSectionsClickable(True)
        self.header().setSectionsMovable(False)
        self.header().setHighlightSections(False)
        # Set default selection model
    def setModel(self, model):
        super(TreeView, self).setModel(model)
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.header().setStretchLastSection(False)
        self.header().setSortIndicatorShown(True)
        self.header().setSortIndicator(0, Qt.SortOrder.AscendingOrder)
        self.header().setSectionsClickable(True)
        self.header().setSectionsMovable(False)
        self.header().setHighlightSections(False)


# Wrapper class for QStandardItem
class StandardItem(QStandardItem):
    def __init__(self, txt='',font_size=12, set_bold=False, set_color=None, set_background_color=None, align=Qt.AlignmentFlag.AlignCenter):
        super().__init__()

        if set_background_color is not None:
            self.setBackground(set_background_color)


        if set_color is not None:
            self.setForeground(set_color)

        font = QFont()
        font.setPointSize(font_size)
        font.setBold(set_bold)
        self.setFont(font)
        # set background color to transparent
        # palette = QPalette()
        # palette.setBrush(QPalette.ColorRole.Base, QBrush(set_background_color))
        self.setText(str(txt))
        self.setTextAlignment(align)
    
    def __lt__(self, otherItem):
        try:
            return float( self.text(self) ) > float( otherItem.text(otherItem) )
        except ValueError:
            return self.text(self) > otherItem.text(otherItem)

    def set_color(self, color):
        self.setForeground(QBrush(color))
