#!/usr/bin/python

from coderwriter import CodeWriter
from parser import Parser
from definitions import *
import os
import sys


def main(codewriter, parser):
    while True:
        command = parser.get_command().strip()
        commandtype = parser.commandType()
        if commandtype == C_ARITHMETIC:
            codewriter.writeArithmetic(command)
        else:
            command = parser.arg1()
            # return is only one command, thus there is no arg2 and it could lead to errors
            if commandtype == C_RETURN:
                codewriter.writeReturn()
            else:
                name = parser.arg2()  # could be name of segment, or name of label and so on
                if commandtype == C_LABEL:
                    codewriter.writeLabel(name)
                elif commandtype == C_IF:
                    codewriter.writeIf(name)
                elif commandtype == C_GOTO:
                    codewriter.writeGoto(name)
                elif commandtype == C_FUNCTION:
                    index = parser.arg3()
                    codewriter.writeFunction(name, index)
                elif commandtype == C_CALL:
                    index = parser.arg3()
                    codewriter.writeCall(name, index)
                else:
                    index = parser.arg3()
                    codewriter.writePushPop(command, name, index)
        if not parser.advance():
            break


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename_ = sys.argv[1]
    else:
        raise TypeError("No directory/file specified")
    codewriter_ = CodeWriter(filename_)
    if os.path.isdir(filename_):
        codewriter_.setFileName("Sys.vm")
        codewriter_.current_function = "Sys.init"
        codewriter_.writeInit()  # there must be Sys.vm file
        for file in os.listdir(filename_):
            codewriter_.setFileName(file)
            file = filename_ + '/' + file
            parser_ = Parser(file)
            main(codewriter_, parser_)
    codewriter_.close()
