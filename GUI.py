# imports
import sys
from PySide6 import QtCore, QtWidgets, QtGui


class Input_Box(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.input_box = QtWidgets.QTextEdit()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.input_box)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Input_Box()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())