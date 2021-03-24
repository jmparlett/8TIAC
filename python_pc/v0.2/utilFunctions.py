'''' 
The is file contains helper functions for the 8TIAC's GUI and other interfaces
'''
#Validate a list of binary instructions
def validateInstructionList(instructionList):
    for instruction in instructionList:
        if len(instruction)==8:
            try:
                int(instruction, 2)
            except ValueError:
                return False
        else:
            return False
    return True


def bootstrap(pyPc, instructionList):
    '''
    This functions loads the bootstrap program and then loads a list of instructions to stdIn
    params: pyPc, InstructionList
    pyPc (This should be an instance of the CLU object initialized with all its components)
    InstructionList (This shoud be a python list including binary instructions in the form of strings)
    '''
    bootStrapInstructions = [   "11111110",
                                "01010010",
                                "00000111",
                                "00010011",
                                "10000100",
                                "11101111",
                                "00110010",
                                "11100000",
                                "11100101",
                                "01100000",
                                "01000000",
                                "00001100"  ] #The bootstrap program is discussed in the manual
    for c,instruction in enumerate(bootStrapInstructions):
        pyPc.ram.m[0][c].m.set_v(instruction)    # print([i for i in pyPc.ram.m[0]])
    pyPc.stdIn += instructionList[:]
    pyPc.r1.m.set_v("00000001")
    pyPc.r0.m.set_v("00001100")
    # while pyPc.ir.m.output() != "00001110": #location 14 is the beginning of the users program
    #     stepSingleInstruction(pyPc)



def draw(GUI):
    '''calls the GUI's draw method if it is present'''
    if GUI != None:
        GUI.draw()

