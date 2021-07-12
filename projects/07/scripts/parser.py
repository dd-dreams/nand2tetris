from definitions import *


class Parser:
    def __init__(self, filename):
        self.input_file = [row.strip() for row in open(filename).readlines()]
        self.remove_spaces_comments()
        self.counter = 0  # for counting which line (command) we are on now
        self.__current_command = self.input_file[self.counter]

    def remove_spaces_comments(self):
        updated_input_file = []
        for index in range(len(self.input_file)):
            # line = self.input_file[index].replace(' ', '')
            line = self.input_file[index]
            if '/' in line:  # removing comments
                line = line[:line.index('/')]
            if len(line) != 0 or len(line) >= 2:  # removing redundant lines
                updated_input_file.append(line)
        self.input_file = updated_input_file

    def hasMoreCommands(self):
        if self.counter < len(self.input_file):
            return True
        return False

    def advance(self):
        self.counter += 1
        if self.hasMoreCommands():
            self.__current_command = self.input_file[self.counter]
            return True
        else:
            return False

    def commandType(self):
        if PUSH in self.__current_command:
            return C_PUSH
        elif POP in self.__current_command:
            return C_POP
        elif LABEL in self.__current_command:
            return C_LABEL
        elif IF in self.__current_command:
            return C_IF
        elif FUNCTION in self.__current_command:
            return C_FUNCTION
        elif RETURN in self.__current_command:
            return C_RETURN
        elif CALL in self.__current_command:
            return C_CALL
        else:
            return C_ARITHMETIC

    def arg1(self) -> str:
        """

        :return: returns the arithmetic command
        """
        return self.__current_command.split(' ')[0]

    def arg2(self) -> str:
        """

        :return: returns the segment
        """
        return self.__current_command.split(' ')[1]

    def arg3(self) -> int:
        """
        should only be launched when its not an arithmetic command

        :return: returns the location (if any)
        """
        return int(self.__current_command.split(' ')[2])

    def get_command(self):
        return self.__current_command
