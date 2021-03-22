#made by: Jonathan Parlett
#Purpose: holds main objects and helper functions for the 8TIAC
#Helper functions are things that not necessarily part of the 8 bit computer implementation
#and include helpful functions such as reading a list of instructions into memory

import memory as mem
import ALU as alu_mod
import control_unit as cu
#Helper functions begin
def readProgramToMemory(instructionList):
    pass

def stepSingleInstruction():
    pass

def stepCycle():
    pass
#Helper functions end


#build computer
#CPU Registers
register_0=mem.register()
register_1=mem.register()
register_2=mem.register()
register_3=mem.register()

#Accumulator for ALU
acc=mem.register()

#Temp regestire that holds a value for input b to ALU
#Temp register is always enabled in actuality it does not have an enable wire
tmp=mem.register()
tmp.e=1
#bus 1 sits between temp and input b of ALU it only allows tmp through when it is off
#if enabled bus 1 discards temps input and inputs a 1 into b instead
bus1=cu.bus1(tmp)

#2GB ram
ram=mem.RAM256Byte()

#Memory address register decides which location in memory will referenced for reads and writes
mar=ram.mar

#flags register for use with jump if instruction set in step 5 of ALU instruction or by CLF instruction
flags_register=mem.register()

#Instruction register holds current instruction to be run by CPU
ir=mem.register()
#Instruction address register contrains memory location of instruction to be placed in IR
#Is incremented by one each cycle unless a JMP instruction is given
iar=mem.register()

#Arithmetic Logic Unit performs all math operations 
alu=alu_mod.ALU()

#Control Unit/Control Section interprets instructions given
clu=cu.control_unit(ram,bus1,register_0,register_1,register_2,register_3,acc,tmp,alu, ir, iar, flags_register)


clu=cu.control_unit(ram,bus1,register_0,register_1,register_2,register_3,acc,tmp,alu, ir, iar, flags_register)


if __name__ == "__main__":
    #test code
    #DATA R0        00100000  
    # bytes to load 00000100
    # DATA R1       00100001
    # bytes to load 00001100
    # Add R1,R0     10000100

    instructions = ['00100000','00000100','00100001','00001100', "10000100"]

    ram.s=1
    clu.ram.mar.set_v("00000000")
    clu.ram.write(instructions[0])
    clu.ram.mar.set_v("00000001")
    clu.ram.write(instructions[1])
    clu.ram.mar.set_v("00000010")
    clu.ram.write(instructions[2])
    clu.ram.mar.set_v("00000011")
    clu.ram.write(instructions[3])
    clu.ram.mar.set_v("00000100")
    clu.ram.write(instructions[4])
    clu.ram.mar.set_v("00000000")
    ram.s=0

    # for i in range(5):
    #     print(clu.ram.m[0][i].output())


    for i in range(21):
        clu.step()

    register_0.e=1
    print(register_0.output())