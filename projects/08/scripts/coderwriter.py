from definitions import *


class CodeWriter:
    def __init__(self, name):
        """

        :param: name of the outputted hack assembly file
        :return:
        """
        self.final_name = name
        self.output_file = open(self.final_name + ASM, "w+")
        self.count_loops = 0  # counting how many loops there is
        self.count_retAddrs = 0  # counting how many return addresses there is
        self.current_filename = None
        self.current_function = None

    # ----HANDLING PUSH AND POP COMMAND----
    def write_d_register_push(self, write=True):
        command = "\n@SP\nM=M+1\n" \
                  "A=M-1\nM=D\n"
        if not write:
            return command
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

    def write_d_pop(self, index, segment, isstatic=False):
        """
        since some memory segments doesn't store an address,
        because those memory segments are the address itself, you just need to add their address,
        to the index
        :param index: temp index
        :param segment: which segment
        :param isstatic: specifying if the segment is a static memory segment (boolean)
        :return:
        """
        command = "\n@{0}\nD=A\n".format(index)

        command += "@{0}\nD=A\n".format(segment) if isstatic else "@{0}\nD=D+A\n".format(segment)
        command += "@R13\nM=D\n" \
                   "@SP\nM=M-1\nA=M\nD=M\n" \
                   "@R13\nA=M\nM=D\n"
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

    def push_static(self, index):
        command = "@{0}-static{1}\nD=M".format(self.current_filename, index)

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

    def push_values(self, segment):
        """
        we are using this method when we need the address contained in a memory segment.
        for example, LCL contains the base address of local variables

        :param segment:
        :return:
        """
        command = "@{0}\nD=M\n".format(segment)

        self.output_file.write(command)
        self.write_d_register_push()

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
            if segment == STATIC:
                self.write_d_pop(index, "{0}-static{1}".format(self.current_filename, index), isstatic=True)
            elif segment == TEMP or segment == POINTER:
                self.write_d_pop(index, segment_pointer)
            else:
                self.write_d_register_pop(index, segment_pointer)

    # ---PROJECT 8----
    # helpers
    @staticmethod
    def writeReturnHelper(segment):
        """
        this method is for return command that restores the caller frame

        :param segment: segment to restore
        :return: final command
        """
        return "@R7\nM=M-1\nA=M\nD=M\n@{0}\nM=D\n".format(segment)

    @staticmethod
    def writeCallHelper(segment):
        """
        this method will create the caller frame

        :param segment: segment to push
        :return:
        """
        return "@{0}\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n".format(segment)

    def setFileName(self, filename):
        self.current_filename = filename

    def writeInit(self):
        command = "// Bootstrap\n"
        command += "@256\nD=A\n@SP\nM=D\n"
        self.output_file.write(command)
        self.writeCall("Sys.init", 0)

    def writeLabel(self, name):
        """

        :param name: name of label
        :return: final command
        """
        command = "\n// label {0}{1}\n" \
                  "({0}${1})\n".format(self.current_function, name)

        self.output_file.write(command)

    def writeGoto(self, label):
        """

        :param label: name of label
        :return: final command
        """
        command = "\n// goto {0}{1}\n" \
                  "@{0}${1}\n" \
                  "0;JMP\n".format(self.current_function, label)

        self.output_file.write(command)

    def writeIf(self, label):
        command = "\n// if-goto {0}${1}\n" \
                  "@SP\nAM=M-1\nD=M\n" \
                  "@{0}${1}\nD;JNE\n".format(self.current_function, label)
        self.output_file.write(command)

    def writeFunction(self, name, nvars):
        command = "\n// function {0} {1}\n".format(name, nvars)  # adding comment
        self.current_function = name
        command += "({0})".format(name)  # adding function label
        for _ in range(nvars):  # adding/pushing new local variables to the stack
            command += "@SP\nAM=M+1\nM=0\n"  # creating local variables
        if nvars != 0:
            command += "@SP\nAM=M+1\n"
        command += "\n// " + name + "\n"  # a sign that we finished to initialize local variables

        self.output_file.write(command)

    def writeCall(self, name, nargs):
        command = "\n// call {0}\n".format(name, nargs)
        command += "@{0}$ret.{1}\nD=A\n@SP\nM=M+1\nA=M-1\nM=D\n".format(name, self.count_retAddrs)
        self.output_file.write(command)
        self.push_values(LCL)
        self.push_values(ARG)
        self.push_values(THIS)
        self.push_values(THAT)
        command = "@5\nD=A\n@SP\nD=M-D\n@{0}\nD=D-A\n@ARG\nM=D\n".format(nargs)  # repositions ARG
        command += "@SP\nD=M\n@LCL\nM=D\n"  # repositions LCL
        command += "@{0}\n0;JMP\n".format(name)  # goto functionName
        command += "({0}$ret.{1})\n".format(name, self.count_retAddrs)
        self.output_file.write(command)
        self.count_retAddrs += 1

    def writeReturn(self):
        command = "\n// return\n"
        command += "@LCL\nD=M\n@R7\nM=D\n"  # endFrame
        command += "@5\nA=D-A\nD=M\n@R8\nM=D\n"  # retAddr
        self.output_file.write(command)
        self.write_d_register_pop(0, ARG)
        command = "@ARG\nD=M\n@SP\nM=D+1\n"
        command += self.writeReturnHelper(THAT) + self.writeReturnHelper(THIS) + \
                   self.writeReturnHelper(ARG) + self.writeReturnHelper(LCL)  # reposition memory segments
        command += "@R8\nA=M\n0;JMP\n"  # repositions return address

        self.output_file.write(command)

    def close(self):
        # closes the current output file
        self.output_file.close()
