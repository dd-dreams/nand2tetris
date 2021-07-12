# this file has basic definitions for easier typing in
# other scripts in the folder


ASM = ".asm"

# arithmetic commands
ADD = "add"
SUB = "sub"
NEG = "neg"
EQ = "eq"
GT = "gt"
LT = "lt"
AND = "and"
OR = "or"
NOT = "not"

# memory segments
LCL = "LCL"
ARG = "ARG"
THIS = "THIS"
THAT = "THAT"
CONSTANT = "constant"
STATIC = "static"
TEMP = "temp"
POINTER = "pointer"

# commands
PUSH = "push"
POP = "pop"
LABEL = 'label'
IF = "if-goto"
FUNCTION = "function"
RETURN = "return"
CALL = "call"
COMMENT = '/'
GOTO = "goto"

# other
C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION"
C_RETURN = "C_RETURN"
C_CALL = "C_CALL"
C_GOTO = "C_GOTO"

# start addresses
TEMP_ADDR = 5
STATIC_ADDR = 16
SP_ADDR = 0
LCL_ADDR = 1
ARG_ADDR = 2
THIS_ADDR = 3
THAT_ADDR = 4
POINTER_ADDR = 3  # this is the start. if you get the code, then you will understand why its fine
