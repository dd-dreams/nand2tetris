from constants import PUSH, POP, RETURN, LABEL, GOTO, IF_GOTO, CALL, FUNCTION_VM, THIS, FIELD, VAR, LOCAL


class VMWriter:
    def __init__(self, output_file_obj):
        self.output_file = output_file_obj

    def writePush(self, segment, index: int):
        if segment == FIELD:
            segment = THIS
        if segment == VAR:
            segment = LOCAL
        self.output_file.write(PUSH + segment + " " + str(index) + "\n")

    def writePop(self, segment, index: int):
        if segment == FIELD:
            segment = THIS
        if segment == VAR:
            segment = LOCAL
        self.output_file.write(POP + segment + " " + str(index) + "\n")

    def writeArithmetic(self, command):
        self.output_file.write(command + "\n")

    def writeLabel(self, label):
        self.output_file.write(LABEL + label + "\n")

    def writeGoto(self, label):
        self.output_file.write(GOTO + label + "\n")

    def writeIf(self, label):
        self.output_file.write(IF_GOTO + label + "\n")

    def writeCall(self, name: str, nargs: int):
        self.output_file.write(CALL + name + " " + str(nargs) + "\n")

    def writeFunction(self, name, nlocals: int):
        self.output_file.write(FUNCTION_VM + name + " " + str(nlocals) + "\n")

    def writeReturn(self):
        self.output_file.write(RETURN + "\n")

    def close(self):
        self.output_file.close()
