#8TIAC Manual

## Instructions / assembly language
all Instructions are 8 bit codes. Generally the first 4 bits denote the instruction
and the last 4 denote the target registers

### The first bit denotes an ALU or Non ALU instruction
MSB = 1 denotes ALU:
MSB = 0 denotes non ALU:
next 3 bits are the opcodes

### Alu Instructions
1000 RARB = ADD RA,RB  (Add the Contents of RA and RB and output to RB)

1001 RARB = SHL RA,RB  (Shift RA left and write output to RB)

1010 RARB = SHR RA,RB  (Shift RA right and write output to RB)

1011 RARB = NOT RA,RB  (Write the Inverse byte of RA to RB)

1100 RARB = AND RA,RB  (AND RA and RB and write output to RB)

1101 RARB = OR  RA,RB  (OR RA and RB and write output to RB)

1110 RARB = XOR RA,RB  (XOR RA and RB and put answer in RB)

1111 RARB = CMP RA,RB  (Compare RA and RB)

### Non Alu Instructions
0000 RARB = LD RA,RB      (Load reg B from address in reg A)

0001 RARB = ST RA,RB      (Store contents of register B to address in Register A)

0010 00RB = DATA 00,RB    (Load the contents of the next memory byte into RB)

0011 00RB = JMPR 00,RB    (jump to mem address in RB)

0100 0000 = JMP 00,00     (Jump to mem address in next byte of memory)

0101 CAEZ = JCAEZ Addr    (jump if tested flag is on)

1000 = JC            (Jump if carry)
0100 = JA            (Jump if A larger)
0010 = JE            (Jump if Equal)
0001 = JZ            (Jump if Zero)
0110 0000 = CLF           (Clear flags)

Last 4 bits denote register A and B for non alu instructions
00 = Reg0
01 = Reg1
10 = Reg2
11 = Reg3

## Standard input (stdIn)
    stdIn is a list in the CLU. The first item in this list is removed and input to R3, if ,R3 is empty (all zeros).
    This allows you to handle input by reading from R3. Once input has been used you may zero R3 using XOR.
    This will allow you to handle the next input.
## Memory
The 8TIAC has 256 bytes of memory. Memory is 0 indexed ranging from [0-255]
The first 12 addresses [0-11] in memory are used by the bootstrap program because of this you should use
locations [12-255] for your programs. You may rewrite the first 12 addresses after the bootstrap if you so choose.

## Bootstrap program
This program is used internaly and is executed by the "Read Program to Memory Button"
R0 = index #having an initial value of 14
R1 = 1     #used for incrementation
R2 = 0     #will be used for comparison
R3 = content
These values will be set manually by the bootstrap() function instead of through calls to the 8TIAC


1.  CMP  R3,R2      #if register 3 is still zero after being XOR'ed then there are no new instructions to be loaded
2.  JMP  JE         #Jump if equal
3.  Addr            #Jump address (Location 8)
4.  ST   R0,R3      #By default stdIn is loaded to R3 this stores the current instruction in stdIn to memory location specified by Index
5.  ADD  R1,R0      #increment index by 1
6.  XOR  R3,R3      #zero R3 to allow for next input from stdIn
7.  JMPR 00R2       #Jump to mem location 0

if loop is finished zero registers, clear flags, and jump to beginning of program

8.  XOR  R0,R0       
9.  XOR  R1,R1
10. CLF
11. JMP             Jump to address stored in next byte of memory
12. Addr            Address of beginning of program (Location 11)



BinaryCode.  These Instructions will consume locations [0-11] in memory.
11111110
01010010
00001000
00010011
10000100
11101111
00110010
11100000
11100101
01100000
01000000
00000111


Add two numbers program
1. DATA 00,R0
2. Number to be added
3. DATA 00,R1
4. Number to be added
5. ADD R0,R1
6. DATA 00,R0
7. Location to store result
8. ST R0,R1


00100000
00010000
00100001
01000000
10000001
00100000
00010100
00010001

