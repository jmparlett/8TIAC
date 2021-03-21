def NAND(i1, i2):
    if i1==1 and i2==1:
        return 0
    else:
        return 1

def AND(i1,i2):
    if i1==1 and i2==1:
        return 1
    else:
        return 0

def AND_4x4(i1,i2,i3,i4):
    return AND(AND(AND(i1,i2),i3),i4)

def NOT(i):
    if i==0:
        return 1
    else:
        return 0

def OR(i1,i2):
    if i1==0 and i2==0:
        return 0
    else:
        return 1
def XOR(i1,i2):
    if (i1==1 and i2==1) or (i1==0 and i2==0):
        return 0
    else:
        return 1


def decode_4x16(string):
    a=int(string[0])
    b=int(string[1])
    c=int(string[2])
    d=int(string[3])
    #0000
    if AND_4x4(NOT(a),NOT(b),NOT(c),NOT(d))==1:
        return 0
   
    #0001
    elif AND_4x4(NOT(a),NOT(b),NOT(c),d):
        return 1

    #0010
    elif AND_4x4(NOT(a),NOT(b),c,NOT(d)):
        return 2

    #0011
    elif AND_4x4(NOT(a),NOT(b),c,d):
        return 3

    #0100
    elif AND_4x4(NOT(a),b,NOT(c),NOT(d)):
        return 4

    #0101
    elif AND_4x4(NOT(a),b,NOT(c),d):
        return 5

    #0110
    elif AND_4x4(NOT(a),b,c,NOT(d)):
        return 6

    #0111
    elif AND_4x4(NOT(a),b,c,d):
        return 7

    #1000
    elif AND_4x4(a,NOT(b),NOT(c),NOT(d)):
        return 8

    #1001
    elif AND_4x4(a,NOT(b),NOT(c),NOT(d)):
        return 9

    #1010
    elif AND_4x4(a,NOT(b),c,NOT(d)):
        return 10

    #1011
    elif AND_4x4(a,NOT(b),c,d):
        return 11
        
    #1100
    elif AND_4x4(a,b,NOT(c),NOT(d)):
        return 12

    #1101
    elif AND_4x4(a,b,NOT(c),d):
        return 13

    #1110
    elif AND_4x4(a,b,c,NOT(d)):
        return 14

    #1111
    elif AND_4x4(a,b,c,d):
        return 15


class mem_bit:
    def __init__(self):
        self.o = 0
        self.i = 0
        self.s = 0
    def set_v(self, i):
        g1=NAND(i,self.s)
        g2=NAND(g1,self.s)
        g4=0
        if g2==0:
            g4=1
        elif self.s==0:
            g4=1
        g3=NAND(g1,g4)
        self.o=g3

class mem_byte:
    def __init__(self):
        self.bits=[
            mem_bit(),
            mem_bit(),
            mem_bit(),
            mem_bit(),
            mem_bit(),
            mem_bit(),
            mem_bit(),
            mem_bit(),
        ]
    def set_v(self,bit_vals):
        for c,i in enumerate(self.bits):
            i.s=1
            i.set_v(int(bit_vals[c]))
            i.s=0
    def output(self):
        s=''
        for i in self.bits:
            s+=str(i.o)
        return s

class enabler:
    def __init__(self):
        pass
    def output(self,bit_vals,e=0):
        if e==1:
            s=''
            for bit in bit_vals:
                s+=str(bit)
            return s
        else:
            return 0

class register:
    def __init__(self):
        self.m=mem_byte()
        self.enabler=enabler()
        self.s=0
        self.e=0
    def set_v(self, bit_vals):
        if self.s==1:
            self.m.set_v(bit_vals)
    def output(self):
        if self.e==1:
            return self.enabler.output(self.m.output(),self.e)
        
class MAR256Byte:
    def __init__(self):
        self.m=mem_byte()
        self.s=0

    def set_v(self, bit_vals):
        self.m.s=self.s
        self.m.set_v(bit_vals)
        self.m.s=0

    def output(self):
        return [decode_4x16(self.m.output()[0:4]),decode_4x16(self.m.output()[4:])]

class RAM256Byte:
    def __init__(self):
        self.m=[]
        for i in range(16):
            register_row=[]
            for i2 in range(16):
                register_row.append(register())
            self.m.append(register_row)
        self.mar=MAR256Byte()
        self.s=0
        self.e=0

    #Write to the register specified by MAR the input should be a string of bits '11001100' such as byte.output()
    def write(self,info):
        address=self.mar.output()
        if self.s==1:
            targetMemRegister = self.m[address[0]][address[1]]
            targetMemRegister.s=1
            targetMemRegister.set_v(info)
            targetMemRegister.s=1
            # self.m[addy[0]][addy[1]].set_v(info)

    #Read from location specified by MAR output will be the string of bits at that location '10100011'
    def read(self):
        if self.e==1:
            address=self.mar.output()
            targetMemRegister = self.m[address[0]][address[1]]
            targetMemRegister.e=1
            out=targetMemRegister.output()
            targetMemRegister.e=0
            return out
            # return self.m[address[0]][address[1]].output()