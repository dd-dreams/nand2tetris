

ASM = ".asm"

# definitions
ADD = "add"
SUB = "sub"
NEG = "neg"
EQ = "eq"
GT = "gt"
LT = "lt"
AND = "and"
OR = "not"
NOT = "not"


class CodeWriter:
    def __init__(self, name):
        """

        :param: name of the outputted hack assembly file
        :return:
        """
        self.name = name
        self.output_file = open(name, "w+")

    def write_d_register(self):
        command = "@SP\n" \
                  "A=M+1\nM=D"
        self.output_file(command)

    def writeArithmetic(self, command):
        """
        this method will write arithmetic commands, to-
        the output file. it will also add commands about
        what command it did now.

        :return:
        """
        final = "\n// {0}\n".format(command)  # commenting
        if command == ADD:
            final = "D=D+M"
        elif command == SUB:
            final = "D=D-M"
        elif command == NEG:
            final = "D=-M"
        elif command == EQ:
            final = "JEQ"
        elif command == GT:
            final = "JGT"
        elif command == LT:
            final = "JLT"
        elif command == AND:
            final = "D&M"
        elif command == OR:
            final = "D|M"
        elif command == NOT:
            final = "D=!M"
        self.output_file.write(final)
        self.write_d_register()

    def push(self, segment, index):
        """
        this method is not supported for the following memory segments:
        constant, temp, pointer. they have their own methods.

        this method will push the selected register (i) to the stack
        :return: command for pushing
        """
        command = "\n// push segment i\n"
        command += "@{0}\nD=M\n" \
                  "@{1}\nD=D+M\n" \
                  "@SP\nM=M+1\nA=M-1\n" \
                  "M=D".format(index, segment)

        return command

    def push_constant(self, index):
        command = "\n// push constant i\n"
        command += "@{0}\nD=M\n" \
                   "@SP\nA=M\n" \
                   "M=D+M"

        return command

    def writePushPop(self, command, segment, index):
        pass

    def close(self):
        # closes the current output file
        self.output_file.close()

