from constants import VAR, ARG, STATIC, FIELD


class SymbolTable:
    """
    the construction of a symbol table looks like this:
    {
        var/static/argument/field: {name: {
                                               type: ...,
                                               index: ...
                                            },
                                       ...
                                       ...
                                     }
        ...
    }
    """
    def __init__(self):
        self.__symboltable = {FIELD: {},
                              STATIC: {}}
        self.classname = None

    def startSubroutine(self):
        self.__symboltable[VAR] = {}
        self.__symboltable[ARG] = {}

    def define(self, name: str, type_: str, kind):
        self.__symboltable[kind][name] = {"type": type_, "index": len(self.__symboltable[kind])}

    def VarCount(self, kind: STATIC or FIELD or ARG or VAR) -> int:
        return len(self.__symboltable[kind])

    def KindOf(self, name: str) -> STATIC or FIELD or ARG or VAR:
        for kind in self.__symboltable.keys():
            values = self.__symboltable[kind]
            if name in values:
                return kind

    def TypeOf(self, name: str):
        for kind in self.__symboltable.values():
            if name in kind:
                return kind[name]["type"]

    def IndexOf(self, name: str) -> int:
        for kind in self.__symboltable.values():
            if name in kind:
                return kind[name]["index"]

    def get_symbol_table(self):
        return self.__symboltable

    def set_classname(self, classname: str):
        self.classname = classname

    def get_classname(self):
        return self.classname
