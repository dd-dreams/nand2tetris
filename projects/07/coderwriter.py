from definitions import *


class CodeWriter:
    def __init__(self, name):
        """

        :param: name of the outputted hack assembly file
        :return:
        """
        self.name = name
        self.output_file = open(self.name + ASM, "w+")
        self.count_loops = 0

    # ----HANDLING PUSH AND POP COMMAND----
    def write_d_register_push(self):
        command = "\n@SP\nM=M+1\n" \
                  "A=M-1\nM=D\n"
        self.output_file.write(command)

    def write_d_arithmetic_push(self):
        """
        this is a method for ONLY two values arithmetic commands.
        i cant use the previous one since its working only on one value.
        when i for example use the "add" command, i don't need to do "M=M+1",
        since im losing a slot in the stack
        :return: None
        """
        command = "\n@SP\n" \
                  "A=M-1\nM=D\n"
        self.output_file.write(command)

    def write_d_register_pop(self, index, segment_pointer):
        command = "\n@{0}\nD=A\n" \
                  "@{1}\nD=D+M\n@R13\nM=D\n" \
                  "@SP\nM=M-1\nA=M\nD=M\n" \
                  "@R13\nA=M\nM=D\n".format(index, segment_pointer)
        self.output_file.write(command)

    def write_d_pop(self, index, segment):
        """
        since temp memory segment doesn't store an address,
        because temp is the address itself, you just need to add the temp address,
        to the index
        :param index: temp index
        :param segment:
        :return:
        """
        command = "\n@{0}\nD=A\n" \
                  "@{1}\nD=D+A\n@R13\nM=D\n" \
                  "@SP\nM=M-1\nA=M\nD=M\n" \
                  "@R13\nA=M\nM=D\n".format(index, segment)
        self.output_file.write(command)

    # ----HANDLING COMMANDS----
    def condition_commands(self, command):
        if command == GT:
            condition = "JGT"
        elif command == LT:
            condition = "JLT"
        else:
            condition = "JEQ"
        final = "D=M-D\n" \
                "@TRUE{0}\nD;{1}\n" \
                "@FALSE{0}\n0;JMP\n" \
                "(TRUE{0})\nD=-1\n@PASSFALSE{0}\n0;JMP\n" \
                "(FALSE{0})\nD=0\n" \
                "(PASSFALSE{0})".format(self.count_loops, condition)
        # if we wont count the loops, then a goto label can go to some other address
        # where this label is also named the same
        self.count_loops += 1
        return final

    def writeArithmetic(self, command):
        """
        this method will write arithmetic commands, to-
        the output file. it will also add commands about
        what command it did now.

        :return:
        """
        final = "\n// {0}\n".format(command)  # commenting

        final += "@SP\nAM=M-1\nD=M\nA=A-1\n"  # for two values arithmetic command (doesn't matter in logic commands)
        if command == ADD:
            final += "D=D+M"
        elif command == SUB:
            final += "D=M-D"
        elif command == NEG:
            final += "D=0\n" \
                     "@SP\nA=M\nD=D-M"
        elif command == EQ or command == GT or command == LT:
            final += self.condition_commands(command)
        elif command == AND:
            final += "D=D&M"
        elif command == OR:
            final += "D=D|M"
        elif command == NOT:
            final += "A=A+1\nD=!M"
        self.output_file.write(final)
        if command == NEG or command == NOT:
            self.write_d_register_push()
        else:
            self.write_d_arithmetic_push()

    @staticmethod
    def push(segment, index):
        """
        this method is not supported for the following memory segments:
        constant, temp, static and pointer. they have their own methods.

        this method will push the selected register (i) to the stack
        :return: command for pushing
        """
        command = "@{0}\nD=A\n" \
                  "@{1}\nA=D+M\nD=M".format(index, segment)

        return command

    @staticmethod
    def push_constant(index):
        command = "@{0}\nD=A\n".format(index)

        return command

    @staticmethod
    def push_static(index):
        command = "@{0}\nD=M".format(STATIC_ADDR + index)

        return command

    @staticmethod
    def push_temp(index):
        command = "@{0}\nD=M\n".format(index)

        return command

    @staticmethod
    def push_pointer(index):
        if index == 0:
            command = "@THIS\nD=M"
        else:
            command = "@THAT\nD=M"
        return command

    def writePushPop(self, command, segment, index):
        final = "\n// {0} {1} {2}\n".format(command, segment, index)  # commenting
        segment_pointer = segment  # = segment if segment == LCL or ARG or THIS or THAT
        if segment == "local":
            final += self.push(LCL, index)
            segment_pointer = LCL
        elif segment == "argument":
            final += self.push(ARG, index)
            segment_pointer = ARG
        elif segment == "this":
            final += self.push(THIS, index)
            segment_pointer = THIS
        elif segment == "that":
            final += self.push(THAT, index)
            segment_pointer = THAT
        elif segment == CONSTANT:
            final += self.push_constant(index)
            segment_pointer = index
        elif segment == STATIC:
            final += self.push_static(index)
            segment_pointer = STATIC_ADDR
        elif segment == TEMP:
            final += self.push_temp(TEMP_ADDR + index)
            segment_pointer = TEMP_ADDR
        elif segment == POINTER:
            final += self.push_pointer(index)
            segment_pointer = POINTER_ADDR
        if command == 'push':
            self.output_file.write(final)
            self.write_d_register_push()
        else:  # else command == pop
            final = "\n// {0} {1} {2}\n".format(command, segment, index)  # commenting
            self.output_file.write(final)
            if segment == TEMP or segment == POINTER or segment == STATIC:
                self.write_d_pop(index, segment_pointer)
            else:
                self.write_d_register_pop(index, segment_pointer)

    def close(self):
        # closes the current output file
        self.output_file.close()
