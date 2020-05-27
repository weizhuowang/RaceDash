import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
buttonx = 200
buttony = 40

class DashWin(QMainWindow):
    def __init__(self):
        super(DashWin, self).__init__()
        self.initUI()
        self.setWindowTitle("Customized Dash")
        self.setGeometry(300,300,1000,700)

    def clicked(self):
        self.b2.setText("LapTimesfffffff")

    def initUI(self):
        self.lab_lap = QLabel(self)
        self.lab_lap.setText("LapTime")
        self.lab_lap.move(800,600)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Settings")
        self.b1.setGeometry(0,0,buttonx,buttony)
        self.b1.clicked.connect(self.clicked)

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("LapTimes")
        self.b2.setGeometry(buttonx,0,buttonx,buttony)
        self.b2.clicked.connect(self.clicked)
        
def window():
    app = QApplication(sys.argv)
    w = DashWin()

    w.show()
    sys.exit(app.exec_())

window()