""" Model associated with user constructed pipeline of elements.

Supports the main UI using MVC pattern semantics.  This class proxies the
actual concatenation (pipeline) of SpikeInterface element space of extractors,
pre-processors, sorters, and post-processors.
"""

import PyQt5.QtCore as qc
import PyQt5.QtGui as qg

import config
from spike_element import SpikeElement


class SpikePipelineModel(qc.QAbstractListModel):
    """Used by UI to display pipeline of elements in a decoupled fashion"""

    def __init__(self, element_model):
        """TBD."""
        super().__init__()

        # Underlying data structure proxied by model
        self._elements = []

        self._decorations = [
            qg.QIcon("bin/EXTR.png"),
            qg.QIcon("bin/PREP.png"),
            qg.QIcon("bin/SORT.png"),
            qg.QIcon("bin/POST.png")
        ]

    # Methods sub-classed from QAbstractListModel
    def rowCount(self, parent):
        return len(self._elements)

    def data(self, mod_index, role=qc.Qt.DisplayRole):
        """ Retrieves data facet (role) from model based on positional index"""
        result = None

        if mod_index.isValid() and mod_index.row() < len(self._elements):
            element = self._elements[mod_index.row()]
            if role == qc.Qt.DisplayRole or role == qc.Qt.EditRole:
                result = element.name
            elif role == qc.Qt.DecorationRole:
                result = self._decorations[element.type]
            elif role == config.ELEMENT_ROLE:
                result = element

        return result

    # Convenience methods used by class APIs
    def _has_instance(self, type):
        for element in self._elements:
            if element.type == type:
                return True
        # Generator expression equivalent for future reference
        # return sum(1 for ele in self._elements if ele.type == type)

    def _swap(self, list, pos1, pos2):
        list[pos1], list[pos2] = list[pos2], list[pos1]

    # Methods for other parts of Spikely to manipulate pipeline
    def run(self):
        """Causes SpikeInterface APIs to be executed on pipeline"""
        pass

    def clear(self):
        """Removes all elements from pipeline"""
        self.beginResetModel()
        self._elements.clear()
        self.endResetModel()

    def add_element(self, element):
        """ Adds element at top of stage associated w/ element type"""
        # Only allow one Extractor or Sorter
        if element.type == config.EXTRACTOR or element.type == config.SORTER:
            if self._has_instance(element.type):
                config.status_bar.showMessage(
                    "Only one instance of that element type allowed",
                    config.TIMEOUT)
                return
        # A bit hacky since it assumes order of type constants
        i = 0
        while (i < len(self._elements) and
                element.type >= self._elements[i].type):
            i += 1
        self.beginInsertRows(qc.QModelIndex(), i, i)
        # Need a deep copy of element to support multi-instance element use
        self._elements.insert(i, SpikeElement(element))
        self.endInsertRows()

    def move_up(self, element):
        i = self._elements.index(element)
        # Elements confined to their stage
        if i > 0 and self._elements[i].type == self._elements[i-1].type:
            self.beginMoveRows(qc.QModelIndex(), i, i, qc.QModelIndex(), i-1)
            self._swap(self._elements, i, i-1)
            self.endMoveRows()
        else:
            config.status_bar.showMessage(
                "Cannot move element any higher", config.TIMEOUT)

    def move_down(self, element):
        i = self._elements.index(element)
        # Elements confined to their stage
        if (i < (len(self._elements) - 1) and
                self._elements[i].type == self._elements[i+1].type):
            # beginMoveRows behavior is fubar if move down from source to dest
            self.beginMoveRows(qc.QModelIndex(), i+1, i+1, qc.QModelIndex(), i)
            self._swap(self._elements, i, i+1)
            self.endMoveRows()
        else:
            config.status_bar.showMessage(
                "Cannot move element any lower", config.TIMEOUT)

    def delete(self, element):
        index = self._elements.index(element)
        self.beginRemoveRows(qc.QModelIndex(), index, index)
        self._elements.pop(index)
        self.endRemoveRows()
