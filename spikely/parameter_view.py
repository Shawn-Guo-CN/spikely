"""Creates an MVC view-control for configuring pipeline element properties.

The Configure Element view/control consists of widgets responsible for
viewing and editing the properties of elements (extractors, sorters, etc.).
"""

import PyQt5.QtWidgets as qw

from .config import PARAM_COL, TYPE_COL, VALUE_COL


class ParameterView(qw.QGroupBox):

    def __init__(self, pipeline_model, element_model):
        super().__init__("Configure Elements")
        self._pipeline_model = pipeline_model
        self._element_model = element_model

        self._init_ui()

    def _init_ui(self):
        self.setLayout(qw.QHBoxLayout())

        cfg_table = qw.QTableView(self)

        # Magic happens here: links element model to view
        cfg_table.setModel(self._element_model)

        cfg_table.verticalHeader().hide()
        cfg_table.setColumnWidth(PARAM_COL, 200)
        cfg_table.setColumnWidth(TYPE_COL, 100)
        cfg_table.setColumnWidth(VALUE_COL, 200)
        cfg_table.horizontalHeader().setStretchLastSection(True)

        self.layout().addWidget(cfg_table)
