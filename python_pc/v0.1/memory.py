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
    def set_v(self, i, s=0):
        g1=NAND(i,s)
        g2=NAND(g1,s)
        g4=0
        if g2==0:
            g4=1
        elif s==0:
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
        self.s=0
    def set_v(self,bit_vals,s=0):
        if s==1:
            for c,i in enumerate(self.bits):
                i.set_v(int(bit_vals[c]),s)
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

    def set_v(self, bit_vals, s=0, e=0):
        self.m.set_v(bit_vals,s)
        return self.enabler.output(self.m.output(),e)
        
class MAR256Byte:
    def __init__(self):
        self.m=mem_byte()

    def set_v(self, bit_vals, s=0):
        self.m.set_v(bit_vals,s)

    def output(self):
        return [decode_4x16(self.m.output()[0:4]),decode_4x16(self.m.output()[4:])]

class RAM256Byte:
    def __init__(self):
        self.m=[]
        for i in range(16):
            byterow=[]
            for i2 in range(16):
                byterow.append(mem_byte())
            self.m.append(byterow)
        self.mar=MAR256Byte()
    def write(self,mem_location,info):
        self.mar.set_v(mem_location,1)
        addy=self.mar.output()
        self.m[addy[0]][addy[1]].set_v(info,1)

    def read(self,mem_location):
        self.mar.set_v(mem_location,1)
        addy=self.mar.output()
        return self.m[addy[0]][addy[1]].output()


# memory=RAM256Byte()

# memory.write('00000000','10001100')
# print(memory.read('00000000'))

# memory.write('00000001','10001110')
# print(memory.read('00000001'))

# memory.write('00000010','10101100')
# print(memory.read('00000010'))

# memory.write('00000011','11101100')
# print(memory.read('00000011'))
