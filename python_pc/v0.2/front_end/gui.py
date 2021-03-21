#add parent dir contain pypc files
import os
parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.append(parent_path)

import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyPcGui
from pyPc import clu as pythonPc
from itertools import chain






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

            #generate lists for table columns.
            setBits= list(chain.from_iterable([[str(register.s) for register in register_row] for register_row in pythonPc.ram.m]))     #column 1
            enableBits= list(chain.from_iterable([[str(register.e) for register in register_row] for register_row in pythonPc.ram.m]))  #column 2
            byteValues = list(chain.from_iterable([[register.m.output() for register in register_row] for register_row in pythonPc.ram.m])) #column 3
            #Define lists of memory data to be entered into table
            memData = [setBits, enableBits, byteValues]
            for c, i in enumerate(memData):
                print(c)
                for c2, i2 in enumerate(i):
                    self.memoryTable.setItem(c2,c, QtWidgets.QTableWidgetItem(i2))

        def draw(self):
            self.drawMar()
            self.drawMemory()
            #highlight cell MAR is currently pointing to
            self.memoryTable.item(int(pythonPc.mar.m.output(), 2), 2).setBackground(QColor(100,100,150))

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PyPcGui()
    window.draw()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()