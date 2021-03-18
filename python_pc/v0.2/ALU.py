import memory as mem
import copy as cp

def decode_2x4(string):
    a=int(string[0])
    b=int(string[1])

    #00
    if mem.AND(mem.NOT(a), mem.NOT(b)):
        return 0
    #01
    elif mem.AND(mem.NOT(a), b):
        return 1
    #10
    elif mem.AND(a, mem.NOT(b)):
        return 2

    #11
    elif mem.AND(a, b):
        return 3



def decode_3x8 (string):
    a=int(string[0])
    b=int(string[1])
    c=int(string[2])

    #000
    if mem.AND(mem.AND(mem.NOT(a),mem.NOT(b)),mem.NOT(c)):
        return 0
    #001
    elif mem.AND(mem.AND(mem.NOT(a),mem.NOT(b)),c):
        return 1
    #010
    if mem.AND(mem.AND(mem.NOT(a),b),mem.NOT(c)):
        return 2
    #011
    if mem.AND(mem.AND(a,b),mem.NOT(c)):
        return 3
    #100
    if mem.AND(mem.AND(a,mem.NOT(b)),mem.NOT(c)):
        return 4
    #101
    if mem.AND(mem.AND(a,mem.NOT(b)),c):
        return 5
    #110
    if mem.AND(mem.AND(a,b),mem.NOT(c)):
        return 6
    #111
    if mem.AND(mem.AND(a,b),c):
        return 7

def left_shift (byte):
    carry=cp.deepcopy(byte[7])
    mod=cp.deepcopy(byte[0:7])
    mod.insert(0,carry)
    return [mod,carry]

def right_shift (byte):
    carry=cp.deepcopy(byte[0])
    mod=cp.deepcopy(byte[1:8])
    mod.append(carry)
    return [mod,carry]

def inverter (byte):
    outbyte=cp.deepcopy(byte)
    for bit in outbyte:
        bit.s=1
        bit.set_v(mem.NOT(bit.o))
        bit.s=0
    return outbyte

def ANDer(byte1,byte2):
    #And byte1 with byte2 and return contents
    outbyte=mem.mem_byte()
    for i in range(8):
        outbyte.bits[i].s=1
        outbyte.bits[i].set_v(mem.AND(byte1.m.bits[i].o,byte2.m.bits[i].o))
        outbyte.bits[i].s=0
    return outbyte

def ORer(byte1,byte2):
    #OR byte1 with byte2 and return contents
    outbyte=mem.mem_byte()
    for i in range(8):
        outbyte.bits[i].s=1
        outbyte.bits[i].set_v(mem.OR(byte1.bits[i].o,byte2.bits[i].o))
        outbyte.bits[i].s=0
    return outbyte

def XORer(byte1,byte2):
    #XOR byte1 with byte2 and return contents
    outbyte=mem.mem_byte()
    for i in range(8):
        outbyte.bits[i].s=1
        outbyte.bits[i].set_v(mem.XOR(byte1.bits[i].o,byte2.bits[i].o))
        outbyte.bits[i].s=0
    return outbyte

def bit_adder(a, b, carry=0):
    #from two bits compute the sum and the carry and return them in a list first item is sum second is carry
    return [mem.XOR(mem.XOR(a.o, b.o),carry),(mem.OR(mem.AND(mem.XOR(a.o,b.o),carry),mem.AND(a.o, b.o)))]

def byte_ADDer(byte1, byte2, i_carry=0):
    #add bits in r1 and r2 and put result back in r1
    carry=i_carry
    outbyte=mem.mem_byte()
    for i in range(8):
        #copy results of adder func to variable
        result = bit_adder(byte1.bits[-i],byte2.bits[-i],carry)
        #set value of bit in r1 to sum
        outbyte.bits[-i].s=1
        outbyte.bits[-i].set_v(result[0])
        outbyte.bits[-i].s=0
        #set carry to carry returned from adder func and proceed to next bit
        carry=result[1]
    #return last carry value to be passed to byte adder function if adding multiple bytes    
    return [outbyte,carry]

def is_zero(byte):
    return mem.NOT(mem.OR(mem.OR(mem.OR(mem.OR(mem.OR(mem.OR(mem.OR(byte.bits[0],byte.bits[1]),byte.bits[2]),byte.bits[3]),byte.bits[4]),byte.bits[5]),byte.bits[6]),byte.bits[7]))

def comparator (a, b, is_equal_i=1, a_larger_i=0):
    #Set initial values
    is_equal=is_equal_i
    a_larger=a_larger_i
    
    #iter over each pair of bits and compare values exit loop if a_larger==1
    #proceed only if is_equal==1
    for i in range(8):
        if a_larger==1 or is_equal==0:
            break
        g1=mem.XOR(a.bits[i].o,b.bits[i].o)
        g2=mem.NOT(g1)
        g3=mem.AND(g2,is_equal)
        g4=mem.AND(mem.AND(is_equal,a.bits[i].o),g1)
        g5=mem.OR(g4,a_larger)
        is_equal=cp.copy(g3)
        a_larger=cp.copy(g5)

    #return values will set properties of ALU
    # is_equal and a_larger = 0 then b is larger
    return [is_equal, a_larger]
class ALU:
    def __init__(self):
        self.opcode=0
        self.byte_a=mem.mem_byte()
        self.byte_b=mem.mem_byte()
        self.last_result=mem.mem_byte()
        self.carry_out=0
        self.carry_in=0
        self.a_larger=0
        self.equal=0
        self.zero=0
    
    def change_opcode(self,bits):
        self.opcode=decode_3x8(bits)

    def value_in(self, a, b):
        self.byte_a.set_v(a.output())
        self.byte_b.set_v(b.output())
    
    #All single bit operations will operate on byte_a
    def pulse(self):
        #Add
        if self.opcode==0:
            result=byte_ADDer(self.byte_a,self.byte_b, self.carry_in)
            self.carry_out=result[1]
            self.last_result=result[0]
            #if performing an ADD operation outputs for comparison will be 0
            self.a_larger=0
            self.equal=0
            return result[0].output()
        
        #Shift right
        elif self.opcode==1:
            result=right_shift(self.byte_a)
            self.last_result=result
            self.carry_in=self.carry_out=result[1]
            #if performing a Shift operation outputs for comparison will be 0
            self.a_larger=0
            self.equal=0
            return result[0].output()

        #Shift left
        elif self.opcode==2:
            result=left_shift(self.byte_a)
            self.last_result=result
            self.carry_in=self.carry_out=result[1]
            #if performing a Shift operation outputs for comparison will be 0
            self.a_larger=0
            self.equal=0
            return result[0].output()

        #NOTer
        elif self.opcode==3:
            result=inverter(self.byte_a)
            self.last_result=result
            #if performing a NOT operation outputs for comparison and carry will be 0
            self.a_larger=0
            self.equal=0
            self.carry_out=0
            return result.output()

        
        #ANDer
        elif self.opcode==4:
            result=ANDer(self.byte_a,self.byte_b)
            self.last_result=result
            return result.output()

        
        #ORer
        elif self.opcode==5:
            result=ORer(self.byte_a,self.byte_b)
            self.last_result=result
            #if performing a OR operation outputs for comparison and carry will be 0
            self.a_larger=0
            self.equal=0
            self.carry_out=0

            return result.output()
        
        #XORer
        elif self.opcode==6:
            result=XORer(self.byte_a,self.byte_b)
            self.last_result=result
            #if performing a XOR operation outputs for comparison and carry will be 0
            self.a_larger=0
            self.equal=0
            self.carry_out=0
            return result.output()
        
        #Compare
        elif self.opcode==7:
          result=comparator(self.byte_a, self.byte_b)
          self.is_equal=result[0]
          self.a_larger=result[1]
          if result==[0,0]:
              print('byte b is larger')
              self.last_result=self.byte_b

          #if performing a Compare operation output for carry will be 0
          self.carry_out=0
          return result
        
        #set byte_a and byte_b to zero as nothing would be setting them otherwise
        self.byte_a.set_v('00000000')
        self.byte_b.set_v('00000000')

        #if calculation is zero set zero flag
        self.zero=is_zero(self.last_result)

# b1 = mem.mem_byte()
# b1.set_v("00000100")

# b2 = mem.mem_byte()
# b2.set_v("00001100")

# result = byte_ADDer(b1, b2)
# print(result[0].output())