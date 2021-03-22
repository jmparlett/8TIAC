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
