import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget


class CustomQTreeWidgetSortingModified(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.order = 0
        try:
            horizontalHeaders = self.header()
            horizontalHeaders.setSectionsClickable(True)
            horizontalHeaders.sectionClicked.connect(self.sortItems)
        except Exception as e:
            logging.exception(e)

    def sortItems(self, column, order=Qt.AscendingOrder):
        try:
            if self.headerItem().text(column) == "Id":
                int_values = []
                mapping = {}
                for i in range(self.topLevelItemCount()):
                    item = self.topLevelItem(i)
                    int_value = int(item.text(column))
                    int_values.append(int_value)
                    mapping[int_value] = item

                int_values.sort()
                if self.order == 0:
                    self.order = 1
                    int_values.reverse()
                else:
                    self.order = 0
                    int_values.sort()

                for i, value in enumerate(int_values):
                    item = mapping[value]
                    self.takeTopLevelItem(self.indexOfTopLevelItem(item))
                    self.insertTopLevelItem(i, item)
            else:
                if self.order == 0:
                    self.order = 1
                    super().sortItems(column, Qt.DescendingOrder)
                else:
                    self.order = 0
                    super().sortItems(column, Qt.AscendingOrder)
        except BaseException as e:
            logging.exception(e)
