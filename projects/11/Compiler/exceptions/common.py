
class FileNameNotMatchingClassName(Exception):
    def __init__(self, line):
        self.msg = "Filename is not matching the class name at line {}".format(line)
        super().__init__(self.msg)


class RequireSyntax(Exception):
    def __init__(self, line, token):
        self.msg = "{0} is required at line {1}".format(token, line)
        super().__init__(self.msg)


class NoClassError(Exception):
    def __init__(self):
        self.msg = "Class is not present. Make sure you had type class keyword"
        super().__init__(self.msg)


class WrongSyntax(Exception):
    def __init__(self, line, token):
        self.msg = "Wrong syntax at line {0} with token \"{1}\"".format(line, token)
        super().__init__(self.msg)


class TypeDoesNotExist(Exception):
    def __init__(self, line, token):
        self.msg = "Type \"{0}\" does not exist. Line: {1}".format(token, line)
        super().__init__(self.msg)


class MissingCurlyBrackets(Exception):
    def __init__(self):
        self.msg = "There are missing curly brackets"
        super().__init__(self.msg)
