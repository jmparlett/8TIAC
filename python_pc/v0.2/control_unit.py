import memory as mem
import ALU as alu_mod

class bus1:
    def __init__(self, tmp):
        self.status=0
        self.tmp=tmp
    def output(self):
        if self.status==0:
            return self.tmp.output()
        elif self.status==1:
            return '00000001'

class control_unit:
    def __init__(self, memory, bus1, r0, r1, r2, r3, acc, tmp, alu, ir, iar,flags_reg):
        self.ram=memory
        self.r0=r0
        self.r1=r1
        self.r2=r2
        self.r3=r3
        self.acc=acc
        self.tmp=tmp
        self.bus1=bus1
        self.alu=alu
        self.mar=self.ram.mar
        self.ir=ir
        self.iar=iar
        self.flags_reg=flags_reg
        self.stdIn=[]

        self.current_step=0
    
    #Internal method to inspect the relevant bits in instruction and determine the appropriate register
    def determine_reg_a(self,s):
        #determine reg_a
        #if reg_a = r0
        if alu_mod.decode_2x4(s[4:6])==0:
            return self.r0

        #if reg_a = r1
        elif alu_mod.decode_2x4(s[4:6])==1:
            return self.r1

        #if reg_a = r2
        elif alu_mod.decode_2x4(s[4:6])==2:
            return self.r2

        #if reg_a = r3
        elif alu_mod.decode_2x4(s[4:6])==3:
            return self.r3
    
    #Internal method to inspect the relevant bits in instruction and determine the appropriate register
    def determine_reg_b(self,s):
        #if reg_b = r0
        if alu_mod.decode_2x4(s[6:8])==0:
            return self.r0

        #if reg_b = r1
        elif alu_mod.decode_2x4(s[6:8])==1:
            return self.r1

        #if reg_b = r2
        elif alu_mod.decode_2x4(s[6:8])==2:
            return self.r2

        #if reg_b = r3
        elif alu_mod.decode_2x4(s[6:8])==3:
            return self.r3

    #Internal function to test flags based on instruction given
    def test_flags(self, s):
        self.flags_reg.e=1
        flags=self.flags_reg.output()
        self.flags_reg.e=0
        C=int(flags[0])
        A=int(flags[1])
        E=int(flags[2])
        Z=int(flags[3])

        # 0000 no checks
        if s=='0000':
            return 0

        # 0001 if Z
        elif s=='0001':
            return Z
        
        # 0010 if E
        elif s=='0010':
            return E
        
        # 0011 if E AND Z
        elif s=='0011':
            return mem.AND(E, Z)

        # 0100 if A
        elif s=='0100':
            return A

        # 0101 if A AND Z
        elif s=='0101':
            return mem.AND(A, Z)

        # 0110 if A AND E
        elif s=='0110':
            return mem.AND(A, E)
   
        # 0111 if A AND E AND Z
        elif s=='0111':
            return mem.AND(mem.AND(A, E), Z)
   
        # 1000 if C
        elif s=='1000':
            return C
   
        # 1001 if C AND Z 
        elif s=='1001':
            return mem.AND(C, Z)
   
        # 1010 if C AND E
        elif s=='1010':
            return mem.AND(C, E)
   
        # 1011 if C AND E AND Z
        elif s=='1011':
            return mem.AND(mem.AND(C, E), Z)
   
        # 1100 if C AND A
        elif s=='1100':
            return mem.AND(C, A)
   
        # 1101 if C AND A AND Z
        elif s=='1101':
            return mem.AND(mem.AND(C, A), Z)
   
        # 1110 if C AND A AND E
        elif s=='1110':
            return mem.AND(mem.AND(C, A), E)
   
        # 1111 if C AND A AND E AND Z
        elif s=='1111':
            return mem.AND_4x4(C, A, E, Z)


    def step(self):
        #Monitoring block start
        # self.ir.e=1
        # print(f'IR contains {self.ir.output()}','\n',f'current step is {self.current_step}','\n')
        # self.ir.e=0
        #Monitoring block end
        self.current_step+=1
        if self.current_step==7:
            self.current_step=0
        else:
            if self.current_step==1:
            #if there is input on std in then input to register 3
                if len(self.stdIn) > 0:
                    self.r3.s=1
                    self.r3.set_v(self.stdIn.pop(0))
                    self.r3.s=0

            #set appropriate s and e bit values for components
                self.mar.s=1
                self.acc.s=1
                self.iar.e=1
                self.ram.e=1

                #enable bus1
                self.bus1.status=1

                #set one into the alu's second input
                self.alu.byte_b.set_v(self.bus1.output())
                #assign MAR to address in IAR
                self.mar.set_v(self.iar.output())

                #assign alu first input to IAR
                self.alu.byte_a.set_v(self.iar.output())

                #assign accumulator to ALU return value
                self.acc.set_v(self.alu.pulse())

                #unset e and s values for components
                self.mar.s=0
                self.acc.s=0
                self.iar.e=0
                self.ram.e=0

                #disable bus1
                self.bus1.status=0

            elif self.current_step==2:
                #set s and e for components
                self.ram.e=1
                self.ir.s=1

                #read from RAM and input to IR
                self.ir.set_v(self.ram.read())

                #unset s and e components
                self.ram.e=0
                self.ir.s=0

            elif self.current_step==3:
                #set s and e for components
                self.acc.e=1
                self.iar.s=1

                #read from ACC and input to IAR
                self.iar.set_v(self.acc.output())

                #unset s and e for components
                self.acc.e=0
                self.iar.s=0

            elif self.current_step==4:
                #set s and e for components
                self.ir.e=1

                #read from instruction register
                instruction=self.ir.output()
                #if first bit in IR is a one it is an ALU instruction

                #begin ALU block
                if int(instruction[0])==1:
                    #determine register b by inspecting last two bits of opcode
                    reg_b=self.determine_reg_b(instruction)

                    #set s and e for components
                    reg_b.e=1
                    self.tmp.s=1

                    #read from reg b input to tmp
                    self.tmp.set_v(reg_b.output())

                    #unset s and e for components
                    reg_b.e=0
                    self.tmp.s=0
                #end ALU block

                #begin non-ALU block
                elif int(instruction[0])==0:
                    #if LD or ST Move from reg_a to MAR
                    if alu_mod.decode_3x8(instruction[1:4])==0 or alu_mod.decode_3x8(instruction[1:4])==1 :
                        reg_a=self.determine_reg_a(instruction)

                        #set s and e
                        reg_a.e=1
                        self.mar.s=1

                        #write from reg_a to MAR
                        self.mar.set_v(reg_a.output())

                        #unset s and e
                        reg_a.e=0
                        self.mar.s=0
                    #if DATA
                    elif alu_mod.decode_3x8(instruction[1:4])==2:
                        #move IAR to MAR and into ALU input a
                        #enable bus 1 output to ALU input b
                        #pulse ALU output to ACC

                        #set s and e
                        self.iar.e=1
                        self.mar.s=1
                        self.acc.s=1
                        #enable bus 1
                        self.bus1.status=1

                        self.mar.set_v(self.iar.output())
                        self.alu.byte_a.set_v(self.iar.output())
                        self.alu.byte_b.set_v(self.bus1.output())
                        self.acc.set_v(self.alu.pulse())

                        #unset s and e
                        self.iar.e=0
                        self.mar.s=0
                        self.acc.s=0

                    #if JMPR
                    elif alu_mod.decode_3x8(instruction[1:4])==3:
                        #move contents of reg_b to IAR
                        reg_b=self.determine_reg_b(instruction)

                        #set s and e
                        reg_b.e=1
                        self.iar.s=1

                        #write from reg_b to IAR
                        self.iar.set_v(reg_b.output())

                        #unset s and e
                        reg_b.e=0
                        self.iar.s=0

                    #if JMP (skip next mem location)
                    elif alu_mod.decode_3x8(instruction[1:4])==4:
                        #read from IAR to MAR

                        #set s and e
                        self.iar.e=1
                        self.mar.s=1

                        #read from IAR to MAR
                        self.mar.set_v(self.iar.output())

                        #unset s and e
                        self.iar.e=0
                        self.mar.s=0

                    #if JCAEZ (jump if tested flag is present)
                    elif alu_mod.decode_3x8(instruction[1:4])==5:
                        #write IAR to MAR and IAR+1 to ACC

                        #set s and e/enable bus1
                        self.bus1.status=1
                        self.iar.e=1
                        self.acc.s=1

                        #read IAR and bus1 into inputs a and b of ALU
                        self.alu.byte_a.set_v(self.iar.output())
                        self.alu.byte_b.set_v(self.bus1.output())
                        #read ALU out into ACC
                        self.acc.set_v(self.alu.pulse())
                        
                        #unset s and e/disable bus1
                        self.bus1.status=0
                        self.iar.e=0
                        self.acc.s=0
                        
                    #if CLF (clear flags)
                    elif alu_mod.decode_3x8(instruction[1:4])==6:
                        #enable bus 1 and pulse the ALU then set the flag register
                        #set s and e/enable bus1
                        self.flags_reg.s=1
                        self.bus1.status=1

                        #pulse ALU and set flags_reg
                        self.alu.byte_b.set_v(self.bus1.output())
                        self.alu.pulse()
                        self.flags_reg.set_v(f'{str(self.alu.carry_out)}{str(self.alu.a_larger)}{str(self.alu.equal)}{self.alu.zero}0000')

                        #unset s and e
                        self.flags_reg.s=0
                        self.bus1.status=0

                #end non-ALU block

                #unset s and e for components
                self.ir.e=0

            elif self.current_step==5:
                #set s and e for components
                self.ir.e=1

                #read from instruction register
                instruction=self.ir.output()
                #if first bit in IR is a one it is an ALU instruction

                #begin ALU block
                if int(instruction[0])==1:
                    #change opcode of alu based on IR
                    self.alu.change_opcode(instruction[1:4])

                    #determine reg_a
                    reg_a=self.determine_reg_a(instruction)
                    #set s and e for components
                    reg_a.e=1

                    #read reg_a into byte_a of ALU
                    self.alu.byte_a.set_v(reg_a.output())

                    #bus1 outputs to ALU byte_b
                    self.alu.byte_b.set_v(self.bus1.output())

                    #unset s and e for components
                    reg_a.e=0

                    #set s and e for components
                    self.acc.s=1

                    #store ALU calculation in ACC
                    self.acc.set_v(self.alu.pulse())
                    #set ALU opcode back to default ADD
                    self.alu.change_opcode('000')
                    #unset s and e for components
                    self.acc.s=0

                    #write to flags register
                    self.flags_reg.s=1
                    self.flags_reg.set_v(f'{str(self.alu.carry_out)}{str(self.alu.a_larger)}{str(self.alu.equal)}{self.alu.zero}0000')
                    self.flags_reg.s=0
                #end ALU block

                #begin non-ALU block
                elif int(instruction[0])==0:
                    #if LD
                    if alu_mod.decode_3x8(instruction[1:4])==0:
                        #Move from RAM to reg_b 
                        reg_b=self.determine_reg_b(instruction)

                        #set s and e
                        reg_b.s=1
                        self.ram.e=1

                        #write from RAM to reg_b
                        reg_b.set_v(self.ram.read())

                        #unset s and e
                        reg_b.s=0
                        self.ram.e=0
                    #if ST
                    elif alu_mod.decode_3x8(instruction[1:4])==1:
                        #Move from reg_b to RAM
                        reg_b=self.determine_reg_b(instruction)

                        #set s and e
                        reg_b.e=1
                        self.ram.s=1

                        #write from reg_b to RAM
                        self.ram.write(reg_b.output())

                        #unset s and e
                        reg_b.e=0
                        self.ram.s=0
                    #if DATA
                    elif alu_mod.decode_3x8(instruction[1:4])==2:
                        #read from RAM to reg_b
                        reg_b=self.determine_reg_b(instruction)

                        #set s and e
                        reg_b.s=1
                        self.ram.e=1

                        #read from RAM to reg_b
                        reg_b.set_v(self.ram.read())

                        #unset s and e
                        reg_b.s=0
                        self.ram.e=0

                    #if JMPR
                    elif alu_mod.decode_3x8(instruction[1:4])==3:
                        #read from RAM to IAR
                        #set s and e
                        self.ram.e=1
                        self.iar.s=1

                        #read from IAR to MAR
                        self.iar.set_v(self.ram.read())

                        #unset s and e
                        self.ram.e=0
                        self.iar.s=0
                    #if JMP
                    elif alu_mod.decode_3x8(instruction[1:4])==4:
                        pass
                    #if JCAEZ (jump if tested flag is present)
                    elif alu_mod.decode_3x8(instruction[1:4])==5:
                        #write ACC to IAR

                        #set s and e
                        self.acc.e=1
                        self.iar.s=1

                        #write ACC to IAR
                        self.iar.set_v(self.acc.output())

                        #unset s and e
                        self.acc.e=0
                        self.iar.s=0
                    #if CLF (clear flags)
                    elif alu_mod.decode_3x8(instruction[1:4])==6:
                        pass
                #end non-ALU block

                #unset IR
                self.ir.e=0

            elif self.current_step==6:
                #set s and e for components
                self.ir.e=1
                print(self.ir.output())

                #read from instruction register
                instruction=self.ir.output()
                #if first bit in IR is a one it is an ALU instruction

                #begin ALU block
                if int(instruction[0])==1:
                    #determine register b by inspecting last two bits of opcode

                    if instruction[1:4]!='111':
                        #if reg_b = r0
                        reg_b=self.determine_reg_b(instruction)

                        #set s and e for components
                        self.acc.e=1
                        reg_b.s=1

                        #read from ACC input to reg_b
                        reg_b.set_v(self.acc.output())

                        #unset s and e for components
                        self.acc.e=0
                        reg_b.s=0
                    #end ALU block

                #begin non-ALU block
                elif int(instruction[0])==0:
                    #if LD
                    if alu_mod.decode_3x8(instruction[1:4])==0:
                        pass
                    #if ST
                    elif alu_mod.decode_3x8(instruction[1:4])==1:
                        pass
                    #if DATA
                    elif alu_mod.decode_3x8(instruction[1:4])==2:
                        #read from ACC to IAR

                        #set s and e
                        self.acc.e=1
                        self.iar.s=1

                        #read from ACC to IAR
                        self.iar.set_v(self.acc.output())

                        #unset s and e
                        self.acc.e=0
                        self.iar.s=0
                    #if JMPR
                    elif alu_mod.decode_3x8(instruction[1:4])==3:
                        pass
                    #if JMP
                    elif alu_mod.decode_3x8(instruction[1:4])==4:
                        pass
                    #if JCAEZ (jump if tested flag is present)
                    elif alu_mod.decode_3x8(instruction[1:4])==5:
                        #if condition is satified write RAM to IAR
                        if self.test_flags(instruction[4:8])==1:
                            #set s and e
                            self.ram.e=1
                            self.iar.s=1

                            #write
                            self.iar.set_v(self.ram.read())

                            #unset s and e
                            self.ram.e=0
                            self.iar.s=0
                            
                    #if CLF (clear flags)
                    elif alu_mod.decode_3x8(instruction[1:4])==6:
                        pass
                #end non-ALU block

                    #Unset s and e for IR
                    self.ir.e=0



