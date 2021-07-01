#!/usr/bin/python

from coderwriter import CodeWriter
from parser import Parser
from definitions import *


def main(codewriter, parser):
    while True:
        command = parser.get_command()
        commandtype = parser.commandType()
        if commandtype == C_ARITHMETIC:
            codewriter.writeArithmetic(command)
        else:
            command = parser.arg1()
            segment = parser.arg2()
            index = parser.arg3()
            codewriter.writePushPop(command, segment, index)
        if not parser.advance():
            break
    codewriter.close()


if __name__ == '__main__':
    filename_ = "StackTest.vm"
    codewriter_ = CodeWriter("StackTest")
    parser_ = Parser(filename_)
    main(codewriter_, parser_)
