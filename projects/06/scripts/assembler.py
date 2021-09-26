from code import Code
from parser import *
from symboltable import SymbolTable


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
        self.__symbols = SymbolTable()
        self.labels_removed = 0  # variable to count how many variables had been removed
        with open(self.__name, 'w+') as file:  # creating an empty file
            pass

    def first_pass(self):
        """
        this pass will check label commands

        :return: 
        """
        for row in range(len(self.__parser.input_file)):
            command = self.__parser.get_command()
            if self.__parser.commandType() == L_COMMAND:
                symbol = self.__parser.symbol() 
                self.labels_removed += 1
                self.__symbols.addEntry(symbol, row - self.labels_removed + 1)
            self.__parser.advance()
        self.__parser.reset_program()  # resetting

    def second_pass(self):
        """
        after dealing with label command, and adding them to-
        the symboltable, we can now actually place them,
        including variables.

        :return:
        """
        for row in range(len(self.__parser.input_file)):
            symbol = self.__parser.symbol()
            command = self.__parser.get_command()
            if '(' in command:  # checking if its a label
                pass           
            elif symbol is not None:  # if its an L/A command
                try:  # checking if specified address (an int)
                    int(symbol)
                    self.__parser.advance()
                    continue
                except ValueError:
                    pass
            
                # if its a variable, we need to assign memory for it

                if not self.__symbols.contains(symbol):
                    available_addr = self.__symbols.get_available_address()
                    self.__symbols.addEntry(str(symbol), available_addr)
                    self.__symbols.available_address += 1
                self.__parser.input_file[row] = '@' + self.__symbols.GetAddress(symbol)
            self.__parser.advance()
        self.__parser.reset_program()

    def output_binary(self):
        with open(self.__name, 'a') as file:
            file.write(self.__current_binary + '\n')

    def convert_decimal_to_binary(self, decimal):  # for A instruction
        decimal = int(decimal)
        self.__current_binary = str(bin(decimal))[2:]  # removing 0b at the beginning
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
            if command_type == L_COMMAND:  # checking if its a label
                self.__parser.advance()
                continue
            elif command_type == A_COMMAND:  # A instruction
                symbol = command[1:]
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
                # creating the instruction
                self.__current_binary += C_INSTRUCTION + comp_binary + dest_binary + jump_binary
            self.output_binary()
            self.__parser.advance()  # going to the next command


def main(filename):
    assembler = Assembler(filename)
    assembler.first_pass()
    assembler.second_pass()
    assembler.translate()

