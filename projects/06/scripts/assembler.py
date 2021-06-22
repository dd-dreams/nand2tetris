from code import Code
from parser import *


# extensions
HACK = ".hack"
C_INSTRUCTION = "111"  # three first binary numbers in instruction
A_INSTRUCTION = "0"
LENGTH_INSTRUCTION = 16


class Assembler:

    def __init__(self, assembly_filename):
        self.__parser = Parser(assembly_filename)
        self.__code = Code()
        self.__name = assembly_filename.split('.')[0] + HACK
        self.__current_binary = ""  # current command in binary
        with open(self.__name, 'w+') as file:
            pass

    def output_binary(self):
        with open(self.__name, 'a') as file:
            file.write(self.__current_binary + '\n')

    def convert_decimal_to_binary(self, decimal):
        decimal = int(decimal)
        self.__current_binary = str(bin(decimal))[2:]
        length = len(self.__current_binary)
        if length < LENGTH_INSTRUCTION:
            self.__current_binary = "0" * (LENGTH_INSTRUCTION - length) + self.__current_binary

    def get_c_fields(self):
        """
        this method will the return the fields of a C instruction
        
        :return: fields
        """

        return self.__parser.dest(), self.__parser.comp(), self.__parser.jump()

    def translate(self):
        while self.__parser.get_end() is False:
            self.__current_binary = ""  # resetting
            command = self.__parser.get_command()  # receiving the command
            command_type = self.__parser.commandType() 
            print(command)
            if command_type == A_COMMAND or command_type == L_COMMAND:  # A/L instruction 
                symbol = self.__parser.symbol()
                self.convert_decimal_to_binary(symbol)
            else:  # C instruction
                dest, comp, jump = self.get_c_fields()   
                if jump is None:  # if there is no jump condition
                   jump = "null"
                if dest != '0':  # when using a conditional jump
                    dest_binary = self.__code.translate_dest(dest)
                else:
                    dest_binary = self.__code.translate_dest("null")
                comp_binary = self.__code.translate_comp(comp)
                jump_binary = self.__code.translate_jump(jump)
                print(comp_binary, dest_binary, jump_binary)
                # creating the instruction
                self.__current_binary += C_INSTRUCTION + comp_binary + dest_binary + jump_binary
            print(self.__current_binary)
            self.output_binary()
            self.__parser.advance()  # going to the next command


def main(filename):
    assembler = Assembler(filename)
    assembler.translate()


if __name__ == '__main__':
    main("PongL.asm")

