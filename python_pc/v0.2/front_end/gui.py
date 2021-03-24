#add parent dir contain pypc files
import os
parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.append(parent_path)

import sys
import pyPcGui
import utilFunctions 
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pyPc import clu as pythonPc
from itertools import chain




class PyPcGui(QtWidgets.QMainWindow, pyPcGui.Ui_MainWindow):
        def __init__(self):
            super().__init__()
            self.setupUi(self)
            self.readProgramToMemoryButton.clicked.connect(self.loadProgram)
            self.stepCycleButton.clicked.connect(self.stepCycle)
            self.stepInstructionButton.clicked.connect(self.stepSingleInstruction)
            # self.btnBrowse.clicked.connect(self.browse_folder)

        def drawMemInfo(self):
            self.marContents.setText(pythonPc.mar.m.output())
            self.memorySetBit.setText(str(pythonPc.ram.s))
            self.memoryEnableBit.setText(str(pythonPc.ram.e))
            #highlight cell MAR is currently pointing to
            self.memoryTable.item(int(pythonPc.mar.m.output(), 2), 3).setBackground(QColor(0, 255, 255))
            #color s and e bits based on value
            sbit=self.memoryTable.item(int(pythonPc.mar.m.output(), 2), 1)
            if sbit.text()=='1':
                sbit.setBackground(QColor(128,255,0))
            else:
                sbit.setBackground(QColor(255, 64, 0))
            ebit=self.memoryTable.item(int(pythonPc.mar.m.output(), 2), 2)
            if ebit.text()=='1':
                ebit.setBackground(QColor(128, 255, 0))
            else:
                ebit.setBackground(QColor(255, 64, 0))

        def drawMemoryContents(self):
            #set num of table rows and colums to accomdate 256 bytes of memory and the appropriate labels for each register
            self.memoryTable.setColumnCount(4)           
            self.memoryTable.setRowCount(256)

            #define and set headers
            headers=['Byte#','Set Bit', 'Enable Bit', 'Value']
            self.memoryTable.setHorizontalHeaderLabels(headers)
            self.memoryTable.setVerticalHeaderLabels(['' for i in range(256)])

            #generate lists for table columns.
            memNums= [str(i) for i in range(256)]
            setBits= list(chain.from_iterable([[str(register.s) for register in register_row] for register_row in pythonPc.ram.m]))     #column 1
            enableBits= list(chain.from_iterable([[str(register.e) for register in register_row] for register_row in pythonPc.ram.m]))  #column 2
            byteValues = list(chain.from_iterable([[register.m.output() for register in register_row] for register_row in pythonPc.ram.m])) #column 3
            #Define lists of memory data to be entered into table
            memData = [memNums,setBits, enableBits, byteValues]
            for c, i in enumerate(memData):
                for c2, i2 in enumerate(i):
                    self.memoryTable.setItem(c2,c, QtWidgets.QTableWidgetItem(i2))
            # print(byteValues)

        #Draw main 4 registers used by Central Logic Unit / Control Section
        def drawRegisters(self):
            #generate lists for table columns.
            setBits = list(map(str, [pythonPc.r0.s, pythonPc.r1.s, pythonPc.r2.s, pythonPc.r3.s]))
            enableBits = list(map(str, [pythonPc.r0.e, pythonPc.r1.e, pythonPc.r2.e, pythonPc.r3.e]))
            byteValues = [pythonPc.r0.m.output(), pythonPc.r1.m.output(), pythonPc.r2.m.output(), pythonPc.r3.m.output()]
            #Define lists of register data to be entered into table
            memData = [setBits, enableBits, byteValues]
            for c, i in enumerate(memData):
                for c2, i2 in enumerate(i):
                    self.regTable.setItem(c2,c, QtWidgets.QTableWidgetItem(i2))
        
        #Display ALU attributes
        def drawALU(self):
            #ALU information is displayed entirely with pyQt labels
            self.currentOpcode.setText(str(pythonPc.alu.opcode))
            b1status= "ON" if pythonPc.bus1.status==1 else "OFF"
            self.bus1Status.setText(b1status)
            self.byteA.setText(pythonPc.alu.byte_a.output())
            self.byteB.setText(pythonPc.alu.byte_b.output())
            self.carryIn.setText(str(pythonPc.alu.carry_in))
            self.carryOut.setText(str(pythonPc.alu.carry_out))
            self.aLargerFlag.setText(str(pythonPc.alu.a_larger))
            self.equalFlag.setText(str(pythonPc.alu.equal))
            self.zeroFlag.setText(str(pythonPc.alu.zero))
            self.accContents.setText(pythonPc.acc.m.output())
        
        #display CLU attributes
        def drawCLU(self):
            #CLU information is displayed entirely with pyQt labels
            self.irContents.setText(pythonPc.ir.m.output())
            self.iarContents.setText(pythonPc.iar.m.output())
            self.currentClockCycle.setText(str(pythonPc.current_step))
            self.flagRegContents.setText(pythonPc.flags_reg.m.output())
            

        def draw(self):
            self.drawRegisters()
            self.drawMemoryContents()
            self.drawMemInfo()
            self.drawALU()
            self.drawCLU()

        def loadProgram(self):
            instructionList = self.programText.toPlainText().split('\n')
            if utilFunctions.validateInstructionList(instructionList):
                self.errorLabel.setText("")    
                utilFunctions.bootstrap(pythonPc, instructionList)
                self.draw()
            else:
                self.errorLabel.setText("Error that is not valid input.\n Please enter 8 digit line seperated binary numbers only.")
        #button functions to step 8TIAC        
        def stepSingleInstruction(self):
            for i in range(7):
                pythonPc.step(self)
            self.draw()
        def stepCycle(self):
            pythonPc.step(self)
            self.draw()
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PyPcGui()
    window.draw()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()