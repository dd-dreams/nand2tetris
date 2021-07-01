# Addresses

STACK BASE ADDRESS = 256 - 2047
STATIC SEGMENT = 16 - 255
TEMP SEGMENT = 5 - 12
General purpose registers = 13 - 15

SP = 0
LCL = 1
ARG = 2 
THIS = 3
THAT = 4

# Formulas

push *segment i* => addr = segmentPointer + i, *SP = *addr, SP++
pop *segment i* => addr = segmentPointer + i, SP--, *SP = *addr

push *constant i* => SP = i, SP++
(no pop of-course, since it's a constant)

assuming a file is called "Foo.vm"
when using static variables, push/pop static i will be
turned into an assembly reference Foo.i (@Foo.i)

push *temp i* => addr = 5 + i, *SP = *addr, SP++

pop *temp i* => addr = 5 + i, SP--, *SP = *addr

push *pointer 0/1* => *SP = THIS/THAT, SP++

pop *pointer 0/1* => SP--, THIS/THAT = *SP

pointer 0 => RAM[3]

pointer 1 => RAM[4]

# Mission for project 7

## <u>Arithmetic / Logical commands</u>

*add*

*sub*

*neg*

*eq*

*get*

*lt*

*and*

*or*

*not*

## <u>Memory access commands</u>

pop *segment i*

push *segment i*

# Mission for project 8

## <u>Branching commands</u>

label *label*

goto *label*

if-goto *label*

## <u>Function commands</u>

function *functionName nVars*

call *functionName nArgs*

# Notice
some files in `assemblies_solutions` aren't updated
