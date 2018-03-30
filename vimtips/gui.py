#!/usr/bin/env python3

import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from .tips import TipHistory
from typing import Optional


class TipsWidget(QtWidgets.QWidget):  # type: ignore
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self._tip_history = TipHistory()
        self._init_ui()
        self.next_tip()

    def _init_ui(self) -> None:
        self._main_layout = QtWidgets.QVBoxLayout()
        self._tip_layout = QtWidgets.QHBoxLayout()
        self._sw_logo = QtSvg.QSvgWidget(os.path.join(os.path.dirname(__file__), 'vimlogo.svg'))
        self._sw_logo.setFixedSize(100, 100)
        self._tip_layout.addWidget(self._sw_logo)
        self._la_tip = QtWidgets.QLabel()
        self._la_tip.setMinimumSize(400, 100)
        self._la_tip.setWordWrap(True)
        self._la_tip.setAlignment(QtCore.Qt.AlignVCenter)
        self._la_tip.setStyleSheet('background-color: white; font-family: monospace; padding: 5px')
        self._tip_layout.addWidget(self._la_tip)
        self._main_layout.addLayout(self._tip_layout)
        self._button_layout = QtWidgets.QHBoxLayout()
        self._pb_previous_tip = QtWidgets.QPushButton('Previous tip')
        self._pb_previous_tip.setEnabled(self._tip_history.has_previous_tip)
        self._pb_previous_tip.clicked.connect(self.previous_tip)
        self._button_layout.addWidget(self._pb_previous_tip)
        self._pb_next_tip = QtWidgets.QPushButton('Next tip')
        self._pb_next_tip.clicked.connect(self.next_tip)
        self._button_layout.addWidget(self._pb_next_tip)
        self._main_layout.addLayout(self._button_layout)
        self.setLayout(self._main_layout)
        self.setWindowTitle('vim tips')
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'vimlogo.svg')))

    def next_tip(self) -> None:
        self._la_tip.setText(self._tip_history.next_tip().tip)
        self._pb_previous_tip.setEnabled(self._tip_history.has_previous_tip)

    def previous_tip(self) -> None:
        try:
            self._la_tip.setText(self._tip_history.previous_tip().tip)
        except TipHistory.NoPreviousTipError:
            pass
        self._pb_previous_tip.setEnabled(self._tip_history.has_previous_tip)


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    w = TipsWidget()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
