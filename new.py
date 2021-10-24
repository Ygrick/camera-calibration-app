from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QScrollArea, QVBoxLayout, QWidget, QMainWindow
from PyQt5.QtGui import QPixmap


class Example(QtWidgets.QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle('ScrollArea')

        self.pxm = QPixmap("fregat-big.png")
        scr = QScrollArea(self)
        pnl = QWidget(self)

        vbox = QVBoxLayout(self)
        for _ in range(5):
            lbl = QLabel()
            lbl.setPixmap(self.pxm)
            vbox.addWidget(lbl)

        pnl.setLayout(vbox)
        scr.setWidget(pnl)
        self.setCentralWidget(scr)
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    mw = Example()
    mw.show()

    app.exec()
