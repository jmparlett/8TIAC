import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyPcGui
import os

path_current = os.path.abspath(__file__)
print(path_current)
current_dir = os.path.dirname(path_current)
desired_dir = os.path.dirname(current_dir)
print(desired_dir)

#add parent dir contain pypc files
os.sys.path.append(desired_dir)

from pyPc import clu as pythonPc



class PyPcGui(QtWidgets.QMainWindow, pyPcGui.Ui_MainWindow):
        def __init__(self):
            super().__init__()
            self.setupUi(self)
            # self.btnBrowse.clicked.connect(self.browse_folder)


        def drawMar(self):
            self.marContents.setText(pythonPc.mar.m.output())
            self.marContents.setAlignment(Qt.AlignCenter)

        def drawMemory(self):
            #set num of table rows and colums to accomdate 256 bytes of memory and the appropriate labels for each register
            self.memoryTable.setColumnCount(3)           
            self.memoryTable.setRowCount(256)

            #define and set headers
            headers=['Set Bit', 'Enable Bit', 'Value']
            self.memoryTable.setHorizontalHeaderLabels(headers)

            #Define lists of memory data to be entered into table
            memData = [['1','2','3','4'],
                       ['1','2','1','3'],
                       ['1','1','2','1']]
            for c, i in enumerate(memData):
                print(c)
                for c2, i2 in enumerate(i):
                    self.memoryTable.setItem(c2,c, QtWidgets.QTableWidgetItem(i2))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PyPcGui()
    window.drawMemory()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()