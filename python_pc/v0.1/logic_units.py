import memory as mem
import copy as cp

def left_shift (source_r,dest_r):
    mod=cp.deepcopy(source_r.m.bits[0:7])
    mod.insert(0,cp.deepcopy(source_r.m.bits[7]))
    dest_r.m.bits=mod

def right_shift (source_r, dest_r):
    mod=cp.deepcopy(source_r.m.bits[1:8])
    mod.append(cp.deepcopy(source_r.m.bits[0]))
    dest_r.m.bits=mod

def inverter (source_r, dest_r):
    i=0
    for bit in dest_r.m.bits:
        bit.set_v(mem.NOT(source_r.m.bits[i].o),1)
        i+=1

def ANDer(r1,r2):
    #And r1 with r2 and put contents back in r1
    for i in range(8):
        r1.m.bits[i].set_v(mem.AND(r1.m.bits[i].o,r2.m.bits[i].o),1)

def ORer(r1,r2):
    #OR r1 with r2 and put contents back in r1
    for i in range(8):
        r1.m.bits[i].set_v(mem.OR(r1.m.bits[i].o,r2.m.bits[i].o),1)

def XORer(r1,r2):
    #XOR r1 with r2 and put contents back in r1
    for i in range(8):
        r1.m.bits[i].set_v(mem.XOR(r1.m.bits[i].o,r2.m.bits[i].o),1)


def bit_adder(a, b, carry=0):
    #from two bits compute the sum and the carry and return them in a list first item is sum second is carry
    return [mem.XOR(mem.XOR(a.o, b.o),carry),(mem.OR(mem.AND(mem.XOR(a.o,b.o),carry),mem.AND(a.o, b.o)))]

def byte_ADDer(r1, r2, i_carry=0):
    #add bits in r1 and r2 and put result back in r1
    carry=i_carry
    for i in range(8):
        #copy results of adder func to variable
        result = bit_adder(r1.m.bits[i],r2.m.bits[i],carry)
        #set value of bit in r1 to sum
        r1.m.bits[i].set_v(result[0], 1)
        #set carry to carry returned from adder func and proceed to next bit
        carry=result[1]
    #return last carry value to be passed to byte adder function if adding multiple bytes    
    return carry

reg1=mem.register()
reg2=mem.register()
reg1.set_v('01100001',1)
reg2.set_v('00000010',1)
# ANDer(reg1,reg2)
byte_ADDer(reg1,reg2,0)
print(reg1.set_v('00000000',0,1))
print(reg2.set_v('00000000',0,1))
# print(reg1.m.bits[7].o)
