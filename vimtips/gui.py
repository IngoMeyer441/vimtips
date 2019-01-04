#!/usr/bin/env python3

import functools
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from .tips import TipHistory, tip_cache_box
from ._version import __version__
from typing import Any, Callable, Optional  # noqa: F401  # pylint: disable=unused-import


class CacheUpdateThread(QtCore.QThread):  # type: ignore
    updated_cache = QtCore.pyqtSignal()

    def __init__(self, target: Callable, slot: Optional[QtCore.pyqtSlot] = None) -> None:
        super().__init__()
        self._target = target
        self._slot = slot
        if self._slot is not None:
            self.updated_cache.connect(self._slot)

    def run(self) -> None:
        self._target()
        self.updated_cache.emit()


class TipsWidget(QtWidgets.QWidget):  # type: ignore
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self._tip_history = TipHistory()
        self._current_cache_update_thread = None  # type: Optional[Any]
        self._cache_updated_at_least_once = False
        self._init_ui()
        self._update_tip_cache_asynchronously()
        self.next_tip()

    def _init_ui(self) -> None:
        self._main_layout = QtWidgets.QVBoxLayout()
        self._tip_layout = QtWidgets.QHBoxLayout()
        self._sw_logo = QtSvg.QSvgWidget(os.path.join(os.path.dirname(__file__), "vimlogo.svg"))
        self._sw_logo.setFixedSize(100, 100)
        self._tip_layout.addWidget(self._sw_logo)
        self._la_tip = QtWidgets.QLabel()
        self._la_tip.setMinimumSize(400, 100)
        self._la_tip.setWordWrap(True)
        self._la_tip.setAlignment(QtCore.Qt.AlignVCenter)
        self._la_tip.setStyleSheet("background-color: white; font-family: monospace; padding: 5px")
        self._tip_layout.addWidget(self._la_tip)
        self._main_layout.addLayout(self._tip_layout)
        self._button_layout = QtWidgets.QHBoxLayout()
        self._pb_previous_tip = QtWidgets.QPushButton("Previous Tip")
        self._pb_previous_tip.setEnabled(self._tip_history.has_previous_tip)
        self._pb_previous_tip.clicked.connect(self.previous_tip)
        self._button_layout.addWidget(self._pb_previous_tip)
        self._pb_next_tip = QtWidgets.QPushButton("Next Tip")
        self._pb_next_tip.clicked.connect(self.next_tip)
        self._button_layout.addWidget(self._pb_next_tip)
        self._main_layout.addLayout(self._button_layout)
        self.setLayout(self._main_layout)
        self.setWindowTitle("Vim Tips v{}".format(__version__))
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), "vimlogo.svg")))
        self.setAttribute(QtCore.Qt.WA_QuitOnClose, on=False)

    def _update_tip_cache_asynchronously(self) -> None:
        thread_type = functools.partial(CacheUpdateThread, slot=self._updated_cache)
        self._current_cache_update_thread = tip_cache_box.update_asynchronously(thread_type=thread_type)

    def next_tip(self) -> None:
        try:
            self._la_tip.setText(self._tip_history.next_tip().tip)
            self._pb_previous_tip.setEnabled(self._tip_history.has_previous_tip)
        except TipHistory.NoNextTipError:
            self._la_tip.setText("No tip available!")
        self.repaint()

    def previous_tip(self) -> None:
        try:
            self._la_tip.setText(self._tip_history.previous_tip().tip)
        except TipHistory.NoPreviousTipError:
            pass
        self._pb_previous_tip.setEnabled(self._tip_history.has_previous_tip)
        self.repaint()

    @QtCore.pyqtSlot()  # type: ignore
    def _updated_cache(self) -> None:
        self._cache_updated_at_least_once = True
        self.setAttribute(QtCore.Qt.WA_QuitOnClose, on=True)
        if self.isHidden():
            self.close()


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    w = TipsWidget()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
