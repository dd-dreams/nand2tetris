from constants import *
from exceptions import common


class CompilationEngine:
    """
    this is CompilationEngine class.
    if you don't understand the code, i suggest you look in the PDF's of project 10, since this code
    is just literally translation english into code.
    """
    def __init__(self, tokenizer, output_file_obj):
        self.tokenizer = tokenizer
        self.output_file = output_file_obj
        self.tabs = 0  # how many tabs to output
        self.count_parentheses_keywords = 0  # counting keywords that their body code uses parentheses like { and }
        self.check_curly_brackets()
        self.compileClass()

    @property
    def current_token(self):
        return self.tokenizer.get_current_token()

    @property
    def count_line(self):
        return self.tokenizer.get_count_line()

    def check_curly_brackets(self):
        """
        this method checks if count({) == count(})
        :return: None
        """
        open_ = 0
        closed = 0
        for line in self.tokenizer.get_file():
            open_ += line.count(OPEN_CURLY)
            closed += line.count(CLOSED_CURLY)
        if open_ != closed:
            raise common.MissingCurlyBrackets

    def output_tag(self, tagtype, content="", open_close=None):
        """

        :param tagtype: what is the tag name
        :param content: content of tag
        :param open_close: do you want to only open a tag and not close or otherway
        :return:
        """
        self.output_file.write("\n" + "  " * self.tabs)
        if open_close is True:
            self.output_file.write("<{}>".format(tagtype))
        elif open_close is False:
            self.output_file.write("</{}>".format(tagtype))
        else:
            self.output_file.write("<{0}> {1} </{0}>".format(tagtype, content))

    def output_and_advance(self, tagtype, content):
        """
        advancing in tokens and outputting tags
        :return:
        """
        self.output_tag(tagtype, content)
        self.tokenizer.advance()

    def compileClass(self):
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == KEYWORD and self.tokenizer.keyWord() == CLASS:
            self.tabs += 1
            self.output_file.write("<class>")
            self.output_and_advance(KEYWORD, CLASS)  # outputting and getting class name
            if self.tokenizer.tokenType() != IDENTIFIER:
                raise common.FileNameNotMatchingClassName(self.count_line)
            self.output_and_advance(IDENTIFIER, self.tokenizer.identifier())  # getting `{`
            if self.tokenizer.tokenType() != SYMBOL:
                raise common.RequireSyntax(OPEN_CURLY, self.count_line)
            self.output_and_advance(SYMBOL, OPEN_CURLY)  # gotta advance before starting to compile class variables
            while self.tokenizer.keyWord() in (FIELD, STATIC):
                self.compileClassVarDec()
            while self.tokenizer.hasMoreTokens():
                self.compileSubroutineDec()
            if self.current_token != CLOSED_CURLY:
                raise common.RequireSyntax(self.count_line, CLOSED_CURLY)
            self.output_tag(SYMBOL, CLOSED_CURLY)
            self.tabs -= 1
            self.output_file.write("\n</class>")
        else:
            raise common.NoClassError
        self.output_file.close()

    def compileClassVarDec(self):
        """

        compiling variables declarations
        you must advance before calling this method, otherwise it could not work-
        since the current token could be not a class declaration but next one could be.
        this term applies to all other compiling methods
        :return:
        """
        if self.tokenizer.tokenType() == KEYWORD:
            keyword = self.tokenizer.keyWord()
            if keyword == STATIC or keyword == FIELD:
                self.output_tag(tagtype="classVarDec", open_close=True)
                self.tabs += 1
                self.compileVarDec(True)
                self.tabs -= 1
                self.output_tag(tagtype="classVarDec", open_close=False)

    def compileSubroutineDec(self):
        if self.current_token == CONSTRUCTOR or self.current_token == FUNCTION or self.current_token == METHOD:
            type_subroutine = self.current_token
            self.output_tag("subroutineDec", open_close=True)
            self.tabs += 1
            # outputting function return type or `constructor` and so on
            self.output_and_advance(KEYWORD, self.tokenizer.keyWord())
            if self.tokenizer.keyWord() not in TYPES and type_subroutine != CONSTRUCTOR:
                raise common.TypeDoesNotExist(self.count_line, self.current_token)
            # advancing to subroutine type
            self.output_and_advance(IDENTIFIER if type_subroutine == CONSTRUCTOR else KEYWORD, self.current_token)
            if not self.tokenizer.tokenType() == IDENTIFIER:
                raise common.RequireSyntax(self.count_line, "Class name")
            self.output_and_advance(IDENTIFIER, self.current_token)  # outputting subroutine name and advancing to `(`
            if not self.tokenizer.tokenType() == SYMBOL:
                raise common.RequireSyntax(self.count_line, OPEN_PARENT)
            self.output_and_advance(SYMBOL, self.current_token)
            self.compileParameterList()
            self.compileSubroutineBody()
            self.tabs -= 1
            self.output_tag(tagtype="subroutineDec", open_close=False)

    def compileParameterList(self):
        self.output_tag(tagtype="parameterList", open_close=True)
        self.tabs += 1
        if self.current_token == CLOSED_PARENT:  # if there are no parameters
            pass
        elif CLOSED_PARENT not in self.tokenizer.get_current_line():  # if closing parenthesis is not present
            raise common.RequireSyntax(self.count_line, CLOSED_PARENT)
        elif self.current_token not in TYPES:  # checking if the current token is something that does not exist
            raise common.TypeDoesNotExist(self.count_line, self.current_token)
        else:  # else as if currently the line is according to grammar
            while self.current_token != CLOSED_PARENT:  # while we didn't reach the end of parameter list
                if self.tokenizer.symbol() == ',':  # if there is another parameter
                    self.output_and_advance(SYMBOL, ',')
                if self.current_token not in TYPES:  # if the type of the variable does not exist (not int or so on)
                    raise common.TypeDoesNotExist(self.count_line, self.current_token)
                self.output_and_advance(KEYWORD, self.current_token)  # outputting the type
                if self.tokenizer.tokenType() != IDENTIFIER:  # checking if varname is an identifier
                    raise common.WrongSyntax(self.count_line, self.current_token)
                self.output_and_advance(IDENTIFIER, self.current_token)
        self.tabs -= 1
        self.output_tag(tagtype="parameterList", open_close=False)
        self.output_and_advance(SYMBOL, self.current_token)  # outputting `)` and leaving parameterList section

    def compileSubroutineBody(self):
        if self.current_token != OPEN_CURLY:
            raise common.WrongSyntax(self.count_line, self.current_token)
        self.output_tag(tagtype="subroutineBody", open_close=True)
        self.tabs += 1
        self.output_and_advance(SYMBOL, self.current_token)  # outputting `(`
        while self.current_token != CLOSED_CURLY:
            if self.current_token == VAR:
                self.compileVarDec()
            else:
                self.compileStatements()
        self.output_tag(SYMBOL, CLOSED_CURLY)
        self.tabs -= 1
        self.output_tag(tagtype="subroutineBody", open_close=False)
        self.tokenizer.advance()  # leaving subroutineBody

    def compileVarDec(self, class_=False):
        """

        :param class_: are we compiling class variables
        :return:
        """
        if self.tokenizer.tokenType() == KEYWORD:
            if not class_:
                self.output_tag("varDec", open_close=True)
                self.tabs += 1
            self.output_and_advance(KEYWORD, self.current_token)
            self.output_tag(IDENTIFIER, self.current_token) if self.tokenizer.tokenType() == IDENTIFIER else \
                self.output_tag(KEYWORD, self.current_token)
            # count how many variables declarations are declared from the same type in same line:
            declarations = self.tokenizer.get_current_line().count(",")
            for _ in range(declarations + 1):  # +1 in case there is only 1 variable declaration
                self.tokenizer.advance()
                self.output_and_advance(IDENTIFIER, self.current_token)
                self.output_tag(SYMBOL, self.current_token) if self.current_token == ',' else None
            if not self.current_token == ';':
                raise common.WrongSyntax(self.count_line, self.current_token)
            self.output_tag(SYMBOL, ";")
            if not class_:
                self.tabs -= 1
                self.output_tag("varDec", open_close=False) if not class_ else None
            self.tokenizer.advance()  # exiting variable declaration

    def compileStatements(self):
        self.output_tag("statements", open_close=True)
        self.tabs += 1
        while self.current_token != CLOSED_CURLY:  # while its not the end of statements
            if self.compileIfWhile():
                self.compileIfWhile()
            self.compileLet()
            self.compileDo()
            self.compileReturn()
        self.tabs -= 1
        self.output_tag("statements", open_close=False)

    def compileLet(self):
        if self.current_token == LET:
            if '=' not in self.tokenizer.get_current_line():
                raise common.WrongSyntax(self.count_line, self.current_token)
            self.output_tag("letStatement", open_close=True)
            self.tabs += 1
            self.output_and_advance(KEYWORD, self.current_token)
            if self.tokenizer.tokenType() != IDENTIFIER:
                raise common.WrongSyntax(self.count_line, self.current_token)
            self.output_and_advance(IDENTIFIER, self.current_token)  # outputting variable name and advancing
            if self.current_token == '[':
                self.output_and_advance(SYMBOL, self.current_token)
                self.compileExpression()
                self.output_and_advance(SYMBOL, self.current_token)
            if self.current_token != '=':  # in case of i think array indexing lol
                self.compileExpression()
            self.output_and_advance(SYMBOL, self.current_token)  # outputting `=` and advancing to expressions
            self.compileExpression()
            if self.current_token == CLOSED_PARENT:  # sometimes in code there can be `(-num);` or something like this
                self.output_and_advance(SYMBOL, CLOSED_CURLY)
            if self.current_token != ';':
                raise common.RequireSyntax(self.count_line, ';')
            self.output_tag(SYMBOL, self.current_token)
            self.tabs -= 1
            self.output_tag("letStatement", open_close=False)
            self.tokenizer.advance()

    def compileIfWhile(self):
        """
        compiling if statement according to PDF
        :return: true if there is an else statement, which tells compileStatements() to call an if statement again
        """
        if self.current_token in (IF, ELSE, WHILE):
            nametag = self.current_token if self.current_token != ELSE else IF
            if self.current_token == IF or self.current_token == WHILE:
                self.output_tag(nametag + "Statement", open_close=True)
                self.tabs += 1
                self.output_tag(KEYWORD, self.current_token)  # outputting `if` or `while`
                if OPEN_PARENT not in self.tokenizer.get_current_line() or CLOSED_PARENT not in self.tokenizer.get_current_line():
                    raise common.RequireSyntax(self.count_line, '( or )')
                self.tokenizer.advance()  # advancing to `(`
                self.output_and_advance(SYMBOL, self.current_token)  # advancing to the expression of `if`
                self.compileExpression()
                if self.current_token != CLOSED_PARENT:
                    raise common.RequireSyntax(self.count_line, CLOSED_PARENT)
            self.output_and_advance(self.tokenizer.tokenType(), self.current_token)
            if self.current_token != OPEN_CURLY:
                raise common.RequireSyntax(self.count_line, OPEN_CURLY)
            self.output_and_advance(SYMBOL, self.current_token)  # outputting `(` and advancing to statements
            self.compileStatements()
            if self.current_token != CLOSED_CURLY:
                raise common.RequireSyntax(self.count_line, CLOSED_CURLY)
            self.output_and_advance(SYMBOL, CLOSED_CURLY)
            if self.current_token == ELSE:
                return True
            self.tabs -= 1
            self.output_tag(nametag + "Statement", open_close=False)

    def compileDo(self):
        if self.current_token == DO:
            if ';' not in self.tokenizer.get_current_line():
                raise common.RequireSyntax(self.count_line, ';')
            self.output_tag("doStatement", open_close=True)
            self.tabs += 1
            self.output_and_advance(KEYWORD, self.current_token)  # outputting `do`
            self.compileTerm(True)
            if self.current_token == CLOSED_PARENT:
                self.output_and_advance(SYMBOL, self.current_token)
            if self.current_token != ';':
                raise common.RequireSyntax(self.count_line, ';')
            self.output_tag(SYMBOL, self.current_token)  # outputting `;`
            self.tabs -= 1
            self.output_tag("doStatement", open_close=False)
            self.tokenizer.advance()

    def compileReturn(self):
        if self.current_token == RETURN:
            self.output_tag("returnStatement", open_close=True)
            self.tabs += 1
            self.output_and_advance(KEYWORD, self.current_token)  # advancing to expressions or `;` (no expression)
            if not self.current_token == ';':
                self.compileExpression()
            if ';' not in self.tokenizer.get_current_line() and self.current_token != ';':
                raise common.RequireSyntax(self.count_line, ';')
            self.output_and_advance(SYMBOL, self.current_token)  # outputting and exiting return line
            self.tabs -= 1
            self.output_tag("returnStatement", open_close=False)

    def compileExpression(self):
        """
        compiling expressions according to PDF project 10.
        we are not calling here advance method because self.compileTerm() is already doing that for us
        :return:
        """
        self.output_tag("expression", open_close=True)
        self.tabs += 1
        # while its not the end of the expression
        while self.current_token not in (OPEN_CURLY, CLOSED_CURLY, ';', CLOSED_PARENT, ']'):
            # equal sign needs to be outside of expression tags; in case of expressionList
            if self.compileTerm() == "=" or self.tokenizer.symbol() == ',':
                break
            if self.current_token in OP:  # op
                if self.current_token == '<':  # can't be outputted since its in XML syntax, so instead:
                    self.output_and_advance(SYMBOL, "&lt;")
                elif self.current_token == '>':  # same
                    self.output_and_advance(SYMBOL, "&gt;")
                elif self.current_token == '&':  # same
                    self.output_and_advance(SYMBOL, "&amp;")
                else:
                    self.output_and_advance(SYMBOL, self.current_token)
        self.tabs -= 1
        self.output_tag("expression", open_close=False)

    def compileTerm(self, do=False):
        """
        compiling term according to PDF
        :param do: boolean, decides if were compiling a `do` keyword also, which then we wont need to print term tag
        :return:
        """
        if self.current_token == "=":  # compileLet method handles this
            return self.current_token
        if not do:
            self.output_tag("term", open_close=True)
            self.tabs += 1
        if self.current_token in UNARY_OP:  # if self.current == `-` or `~`
            self.output_and_advance(SYMBOL, self.current_token)
            self.compileTerm()
        elif self.tokenizer.tokenType() == KEYWORD:  # means it could be a `boolean` or `null` or `this`
            if self.current_token not in keywordConstant:
                raise common.WrongSyntax(self.count_line, self.current_token)
            self.output_and_advance(KEYWORD, self.current_token)
        elif self.tokenizer.tokenType() == STRING_CONST:  # string constant
            self.output_and_advance(STRING_CONST, self.current_token)
        elif self.tokenizer.tokenType() == INT_CONST:  # int constant
            self.output_and_advance(INT_CONST, self.current_token)
        elif self.current_token == OPEN_PARENT:
            self.output_and_advance(SYMBOL, self.current_token)
            self.compileExpression()
            self.output_and_advance(SYMBOL, self.current_token)
        elif self.tokenizer.tokenType() == IDENTIFIER:  # function call or variable names and so on
            self.output_and_advance(IDENTIFIER, self.current_token)  # outputting varname or subroutine name
            if self.current_token == '[':  # means its array indexing
                self.output_and_advance(SYMBOL, self.current_token)
                self.compileExpression()
                if self.current_token != ']':
                    raise common.WrongSyntax(self.count_line, self.current_token)
                self.output_and_advance(SYMBOL, self.current_token)  # outputting `[`
            elif self.current_token == OPEN_PARENT:  # if its subroutineCall or `(expression)`
                self.output_and_advance(SYMBOL, self.current_token)  # outputting `(`
                self.compileExpressionList()
                # self.output_and_advance(SYMBOL, self.current_token)  # outputting `)`
            elif self.current_token == '.':  # if its also a subroutineCall
                self.output_tag(SYMBOL, self.current_token)
                if OPEN_PARENT not in self.tokenizer.get_current_line() or CLOSED_PARENT not in self.tokenizer.get_current_line():
                    raise common.RequireSyntax(self.count_line, '( or )')
                self.tokenizer.advance()  # advancing to method/function name
                self.output_and_advance(IDENTIFIER, self.current_token)  # advancing to `(`
                self.output_and_advance(SYMBOL, self.current_token)  # `(`, advancing to expressionList
                self.compileExpressionList()  # also handling closing of expressionList
                self.output_and_advance(SYMBOL, self.current_token)  # outputting `)`
        if not do:
            self.tabs -= 1
            self.output_tag("term", open_close=False)

    def compileExpressionList(self):
        """
        compiling list of expressions. list of expressions are in format like that: (expression, expressions, ...)
        usually, on other methods there are self.tokenizer.advance() line, so we would exit their part in the current
        line. here we don't need to, since self.compileExpressions() is already handling this
        :return:
        """
        expressions = self.tokenizer.get_current_line().count(',')  # how many expressions are there
        self.output_tag("expressionList", open_close=True)
        self.tabs += 1
        if self.tokenizer.symbol() != ')':  # if there IS an expressionList
            if CLOSED_PARENT not in self.tokenizer.get_current_line():
                raise common.RequireSyntax(self.count_line, CLOSED_PARENT)
            for _ in range(expressions + 1):
                if self.tokenizer.symbol() == ',':
                    self.output_and_advance(SYMBOL, ',')
                self.compileExpression()
        self.tabs -= 1
        self.output_tag("expressionList", open_close=False)
