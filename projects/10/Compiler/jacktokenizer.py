#!/usr/bin/python

from constants import *
import grammar
from exceptions import common
import re


class JackTokenizer:
    def __init__(self, filename):
        self.file = [line.strip() for line in open(filename).readlines()]
        self.removeCommentsWhiteSpace()
        self.count_lines = 0
        self.__current_line = ""
        self.__current_token = ""
        self.tokens = []  # tokens found from re
        self.__current_type = None
        self.reg = re.compile(RE_MATCH_TOKENS)
    
    def hasMoreTokens(self):
        """
        checking if we reached the end of file
        :return:
        """
        if self.count_lines == len(self.file):
            return False
        return True

    def removeCommentsWhiteSpace(self):
        """
        removing all the comments and redundant lines (such as blank lines)

        :return:
        """
        # i had to use another list because the file is changing (removing lines etc)
        updated_file = []
        indexes = []
        is_still_comment = False
        for line in self.file:
            if '*/' in line:
                is_still_comment = False
                continue
            if is_still_comment:
                if len(self.file) == self.file.index(line) + 1:  # */ is a must when using /** kind of comments
                    raise common.RequireSyntax(self.file.index(line), '*/')
                continue
            if len(indexes) != 0:
                indexes.pop()
                continue
            if '//' in line:
                line_index = line.index('//')
            elif '/**' in line:
                is_still_comment = True
                continue
            elif '*/' in line:
                line_index = line.index('*/')
            else:
                # if there are no comments, then set the line index to be set for the full line
                line_index = len(line)
            # remove redundant lines
            if len(line) == 0 or line_index == 0:
                continue
            updated_file.append(line[:line_index].strip())
        self.file = updated_file

    def advance(self):
        # moving to next line
        if len(self.tokens) == 0:
            self.__current_line = self.file[self.count_lines]
            self.count_lines += 1
            self.tokens = self.reg.findall(self.__current_line)
            self.tokens.reverse()  # reversing for pop method
        self.__current_token = self.tokens.pop()
        # removing the current token
        ind = len(self.__current_token)
        self.__current_line = self.__current_line[ind:].strip()
        # checking if its a keyword or a symbol or None
        possib = grammar.is_symbol(self.__current_token)
        if possib is None:  # if there is no such symbol or keywords
            if grammar.integerConstant(self.__current_token):
                self.__current_type = INT_CONST
            elif '"' in self.__current_token:  # if its a string const
                # removing quote and adding the rest of the string
                self.__current_token = self.__current_token[1:]
                self.__current_type = STRING_CONST
            elif self.__current_token in KEYWORDS:
                self.__current_type = KEYWORD
            elif not self.__current_token[0].isdigit():  # according to specifics
                self.__current_type = IDENTIFIER
            else:
                raise common.WrongSyntax(self.count_lines, self.__current_token)

            self.__current_type = KEYWORD if self.__current_token == NULL else self.__current_type
        else:
            self.__current_type = possib

    def tokenType(self):
        """
        return the current type: KEYWORD | IDENTIFIER | SYMBOL | INT | STRING
        :return:
        """
        return self.__current_type

    def keyWord(self):
        """
        returns the current keyword

        :return: current keyword
        """
        return self.__current_token if self.tokenType() == KEYWORD else None

    def symbol(self):
        """
        return the current symbol

        :return: current symbol if the current token is a symbol else None
        """
        return self.__current_token if self.tokenType() == SYMBOL else None

    def intVal(self):
        """
        returns the current int

        :return:
        """
        return self.__current_token if self.tokenType() == INT_CONST else None

    def stringVal(self):
        """
        returns the current string

        :return:
        """
        return self.__current_token if self.tokenType() == STRING_CONST else None

    def identifier(self):
        return self.__current_token if self.tokenType() == IDENTIFIER else None

    def get_count_line(self):
        return self.count_lines

    def get_current_token(self):
        return self.__current_token

    def get_current_line(self):
        return self.__current_line

    def get_file(self):
        return self.file
