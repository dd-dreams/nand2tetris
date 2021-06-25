

# definitions
C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION"
C_RETURN = "C_RETURN"
C_CALL = "C_CALL"
SP = 0
LCL = 1
ARG = 2
THIS = 3
THAT = 4

# addresses
STACK_START = 256
STACK_END = 2047
TEMP_START = 5
TEMP_EN = 12
STATIC_START = 16
START_END = 255
GENERAL_START = 13
GENERAL_END = 15

ADD = "add"
SUB = "sub"
NEG = "neg"
EQ = "eq"
GT = "gt"
LT = "lt"
AND ="and"
OR = "or"
NOT = "NOT"


class Parser:
    def __init__(self, filename):
        self.input_file = [row.strip() for row in open(filename).readlines()]
        self.remove_spaces_comments()
        self.counter = 0  # for counting which line (command) we are on now
        self.__current_command = self.input_file[self.counter]

    def remove_spaces_comments(self):
        updated_input_file = []
        for index in range(len(self.input_file)):
            line = self.input_file[index].replace(SPACE, "")
            if COMMENT in line:  # removing comments
                line = line[:line.index(COMMENT)]
            if len(line) != 0 or len(line) >= 2:  # removing redundant lines
               updated_input_file.append(line)
        self.input_file = updated_input_file

    def hasMoreCommands(self):
        if self.counter < len(self.input_file):
            return True
        return False

    def advance(self):
        if self.hasMoreCommands():
            self.counter += 1
            self.__current_command = self.input_file[self.counter]
        else:
            return False

    def commandType(self):
        if C_PUSH in self.__current_command:
            return C_PUSH
        elif C_POP in self.__current_command:
            return C_POP
        elif C_LABEL in self.__current_command:
            return C_LABEL
        elif C_IF in self.__current_command:
            return C_IF
        elif C_FUNCTION in self.__current_command:
            return C_FUNCTION
        elif C_RETURN in self.__current_command:
            return C_RETURNS
        elif C_CALL in self.__current_command:
            return C_CALL
        else:
            return C_ARITHMETIC

    def arg1(self) -> str:
        return self.__current_command.split(" ")[0]

    def arg2(self) -> int:
        return self.__current_command.split(" ")[1]

