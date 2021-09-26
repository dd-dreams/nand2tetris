
A_COMMAND = "A_COMMAND"
L_COMMAND = "L_COMMAND"
C_COMMAND = "C_COMMAND"
SPACE = " "
COMMENT = "/"


class Parser:
    def __init__(self, input_file):
        self.input_file = [row.strip() for row in open(input_file).readlines()]
        self.counter = 1
        self.remove_spaces_comments()
        self.__current_command = self.input_file[0]
        self.end = False

    def remove_spaces_comments(self):
        updated_input_file = []
        for index in range(len(self.input_file)):
            line = self.input_file[index]
            line = line.replace(SPACE, "")
            if COMMENT in line:  # removing comments
                index_comment = line.index(COMMENT)
                line = line[:index_comment]
            if len(line) != 0 or len(line) > 2:  # removing redundant lines
               updated_input_file.append(line)
        self.input_file = updated_input_file

    def hasMoreCommands(self):
        if self.counter < len(self.input_file):
            return True
        return False

    def advance(self):
        if self.hasMoreCommands():
            self.__current_command = self.input_file[self.counter]
            self.counter += 1
        else:  # if its the end of the program
            self.end = True
            return self.end

    def commandType(self):
        if self.__current_command is None:
            return
        if '@' in self.__current_command: 
            return A_COMMAND 
        elif '(' in self.__current_command:
            return L_COMMAND 
        else:
            return C_COMMAND

    def symbol(self):
        if self.commandType() == A_COMMAND:  # removing @
            return self.__current_command[1:]
        if self.commandType() == L_COMMAND:  # removing parentheses
            return self.__current_command[1:-1]

    def dest(self):
        if self.commandType() == C_COMMAND:
            if '=' in self.__current_command:
                return self.__current_command.split('=')[0]
            else:  # if its a jump condition, then the dest doesn't matter
                # because the dest is line before, when were doing @value
                return "null"

    def comp(self):
        if self.commandType() == C_COMMAND:
            if '=' in self.__current_command:
                return self.__current_command.split('=')[1].split(';')[0]  # splitting fields
            else:  # if there is only jump
                return self.__current_command.split(';')[0]  # splitting fields

    def jump(self):
        if ';' not in self.__current_command:
            return None 
        if self.commandType() == C_COMMAND:
            return self.__current_command.split('=')[0].split(';')[1]  # splitting fields

    def get_input_file(self):
        return self.input_file

    def get_command(self):
        return self.__current_command

    def get_end(self):
        return self.end

    def reset_program(self):
        """
        sometimes we will need to reset the program,
        if we are for example going through the assembly file
        again.

        :return:
        """
        
        self.counter = 1
        self.__current_command = self.input_file[0]
        self.end = False 
