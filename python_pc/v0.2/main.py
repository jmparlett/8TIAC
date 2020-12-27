import memory as mem
import ALU as alu_mod
import control_unit as cu

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


#test code add 2 numbers by stepping the CU
register_0.s=1
register_0.set_v('00000100')
register_0.s=0

register_1.s=1
register_1.set_v('00001100')
register_1.s=0

ram.s=1
ram.write('10000100')
ram.s=0


clu=cu.control_unit(ram,bus1,register_0,register_1,register_2,register_3,acc,tmp,alu, ir, iar, flags_register)


clu.step()
clu.step()
clu.step()
clu.step()
clu.step()
clu.step()
clu.step()

register_0.e=1
print(register_0.output())
