from constants import *
from exceptions import common
from vmwriter import VMWriter
from symboltable import SymbolTable


class CompilationEngine:
    """
    this is CompilationEngine class.
    if you don't understand the code, i suggest you look in the PDF's of project 10, since this code
    is just literally translation english into code.
    """
    def __init__(self, tokenizer, output_file_obj):
        self.__curr_expression = []
        self.output_file = output_file_obj
        self.tokenizer = tokenizer
        self.vmwriter = VMWriter(self.output_file)
        self.symboltable = SymbolTable()

        self.curr_subroutine_name = None
        self.is_subroutine_void = False
        self.subroutine_type = None

        self.count_parentheses_keywords = 0  # counting keywords that their body code uses parentheses like { and }
        self.count_labels = 0
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

    def compileClass(self):
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == KEYWORD and self.tokenizer.keyWord() == CLASS:
            self.tokenizer.advance()
            if self.tokenizer.tokenType() != IDENTIFIER:
                raise common.FileNameNotMatchingClassName(self.count_line)
            self.symboltable.set_classname(self.current_token)
            self.tokenizer.advance()
            if self.tokenizer.tokenType() != SYMBOL:
                raise common.RequireSyntax(OPEN_CURLY, self.count_line)
            self.tokenizer.advance()
            while self.tokenizer.keyWord() in (FIELD, STATIC):
                self.compileClassVarDec()
            while self.tokenizer.hasMoreTokens():
                self.compileSubroutineDec()
            if self.current_token != CLOSED_CURLY:
                raise common.RequireSyntax(self.count_line, CLOSED_CURLY)
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
                self.compileVarDec()

    def compileSubroutineDec(self):
        if self.current_token == CONSTRUCTOR or self.current_token == FUNCTION or self.current_token == METHOD:
            self.subroutine_type = self.current_token
            self.symboltable.startSubroutine()
            self.tokenizer.advance()  # outputting function return type or `constructor` and so on
            if (self.tokenizer.keyWord() not in TYPES and self.symboltable.IndexOf(self.tokenizer.keyWord()) is not None) \
                    and self.subroutine_type != CONSTRUCTOR:
                raise common.TypeDoesNotExist(self.count_line, self.current_token)
            if self.subroutine_type == METHOD:
                self.symboltable.define(THIS, self.symboltable.classname, ARG)
            return_type = self.current_token
            if return_type == VOID:
                self.is_subroutine_void = True
            self.tokenizer.advance()  # advancing to subroutine name
            if not self.tokenizer.tokenType() == IDENTIFIER:
                raise common.RequireSyntax(self.count_line, "Class name")
            self.curr_subroutine_name = self.current_token
            self.tokenizer.advance()
            if not self.tokenizer.tokenType() == SYMBOL:
                raise common.RequireSyntax(self.count_line, OPEN_PARENT)
            self.tokenizer.advance()
            self.compileParameterList()
            self.compileSubroutineBody()
            self.is_subroutine_void = False

    def compileParameterList(self):
        if self.current_token == CLOSED_PARENT:  # if there are no parameters
            pass
        elif self.current_token not in TYPES:  # checking if the current token is something that does not exist
            raise common.TypeDoesNotExist(self.count_line, self.current_token)
        else:  # else as if currently the line is according to grammar
            while self.current_token != CLOSED_PARENT:  # while we didn't reach the end of parameter list
                if self.tokenizer.symbol() == ',':  # if there is another parameter
                    self.tokenizer.advance()
                if self.current_token not in TYPES:  # if the type of the variable does not exist (not int or so on)
                    raise common.TypeDoesNotExist(self.count_line, self.current_token)
                argument_type = self.current_token
                self.tokenizer.advance()
                if self.tokenizer.tokenType() != IDENTIFIER:  # checking if varname is an identifier
                    raise common.WrongSyntax(self.count_line, self.current_token)
                argument_name = self.current_token
                self.tokenizer.advance()
                self.symboltable.define(argument_name, argument_type, ARG)
        self.tokenizer.advance()

    def compileSubroutineBody(self):
        """

        :return: 
        """
        declared_variables = False
        if self.current_token != OPEN_CURLY:
            raise common.WrongSyntax(self.count_line, self.current_token)
        self.tokenizer.advance()
        while self.current_token != CLOSED_CURLY:
            if self.current_token == VAR:
                self.compileVarDec()
            else:
                if not declared_variables:
                    self.vmwriter.writeFunction(self.symboltable.get_classname() + '.' + self.curr_subroutine_name,
                                                self.symboltable.VarCount(VAR))
                    declared_variables = True
                    if self.subroutine_type == CONSTRUCTOR:
                        self.vmwriter.writePush(CONSTANT, self.symboltable.VarCount(FIELD))
                        self.vmwriter.writeCall("Memory.alloc", 1)
                        self.vmwriter.writePop(POINTER, 0)
                    elif self.subroutine_type == METHOD:
                        self.vmwriter.writePush(ARG, 0)  # settings up `this` segment
                        self.vmwriter.writePop(POINTER, 0)
                self.compileStatements()
        self.tokenizer.advance()  # leaving subroutineBody

    def compileVarDec(self):
        """

        :return: how many variables we declared now. useful for writing vm commands.
        """
        if self.tokenizer.tokenType() == KEYWORD:
            token_kind = self.current_token  # if its static or field, meaning its a class variable
            self.tokenizer.advance()
            token_type = self.current_token  # type of the current token(s)
            if self.tokenizer.tokenType() != IDENTIFIER:
                token_type = self.current_token  # type of the current token(s) if its a class variable

            # count how many variables declarations are declared from the same type in same line:
            declarations = self.tokenizer.get_current_line().count(",")
            for _ in range(declarations + 1):  # +1 in case there is only 1 variable declaration
                self.tokenizer.advance()
                token_identifier = self.current_token
                self.symboltable.define(token_identifier, token_type, token_kind)
                self.tokenizer.advance()

            if not self.current_token == ';':
                raise common.WrongSyntax(self.count_line, self.current_token)
            self.tokenizer.advance()  # exiting variable declaration
            return declarations + 1

    def compileStatements(self):
        while self.current_token != CLOSED_CURLY:  # while its not the end of statements
            if self.compileIf():
                self.compileIf()
            self.compileWhile()
            self.compileLet()
            self.compileDo()
            self.compileReturn()

    def compileLet(self):
        if self.current_token == LET:
            if '=' not in self.tokenizer.get_current_line():
                raise common.WrongSyntax(self.count_line, self.current_token)
            self.tokenizer.advance()
            if self.tokenizer.tokenType() != IDENTIFIER:
                raise common.WrongSyntax(self.count_line, self.current_token)
            pop_varname = self.current_token  # variable name to return results to
            self.tokenizer.advance()
            array_assigning = False
            if self.current_token == '[':  # assigning array element
                array_assigning = True
                index_arr = self.symboltable.IndexOf(pop_varname)
                kind_arr = self.symboltable.KindOf(pop_varname)
                self.vmwriter.writePush(kind_arr, index_arr)
                self.tokenizer.advance()
                self.compileExpression()
                self.vmwriter.writeArithmetic(ADD)
                self.tokenizer.advance()
                if self.current_token != '=':  # not sure if its needed
                    self.compileExpression()
            self.tokenizer.advance()
            self.compileExpression()
            if array_assigning:
                self.vmwriter.writePop(TEMP, 0)
                self.vmwriter.writePop(POINTER, 1)
                self.vmwriter.writePush(TEMP, 0)
                self.vmwriter.writePop(THAT, 0)
            if self.current_token == CLOSED_PARENT:  # sometimes in code there can be `(-num);` or something like this
                self.tokenizer.advance()
            if self.current_token != ';':
                raise common.RequireSyntax(self.count_line, ';')
            self.tokenizer.advance()
            segment = self.symboltable.KindOf(pop_varname)
            index = self.symboltable.IndexOf(pop_varname)
            if not array_assigning:
                self.vmwriter.writePop(segment, index)

    def compileWhile(self):
        """
        compiling while statement according to PDF
        :return:
        """
        if self.current_token == WHILE:
            start_loop_label = "L" + str(self.count_labels)
            self.count_labels += 1
            end_loop_label = "L" + str(self.count_labels)
            self.count_labels += 1
            self.vmwriter.writeLabel(start_loop_label)
            if OPEN_PARENT not in self.tokenizer.get_current_line() or CLOSED_PARENT not in \
                    self.tokenizer.get_current_line():
                raise common.RequireSyntax(self.count_line, '( or )')
            self.tokenizer.advance()
            self.tokenizer.advance()
            self.compileExpression()
            if self.current_token != CLOSED_PARENT:
                raise common.RequireSyntax(self.count_line, CLOSED_PARENT)
            self.vmwriter.writeArithmetic(NOT)
            self.vmwriter.writeIf(end_loop_label)
            self.compile_code_blocks()
            self.vmwriter.writeGoto(start_loop_label)
            self.vmwriter.writeLabel(end_loop_label)  # end of while loop

    def compile_code_blocks(self):
        """
        compiling the statements in code blocks like while if or else code blocks
        :return:
        """
        self.tokenizer.advance()
        if self.current_token != OPEN_CURLY:
            raise common.RequireSyntax(self.count_line, OPEN_CURLY)
        self.tokenizer.advance()
        self.compileStatements()
        if self.current_token != CLOSED_CURLY:
            raise common.RequireSyntax(self.count_line, CLOSED_CURLY)
        self.tokenizer.advance()

    def compileIf(self):
        """
        compiling `if` and `else` statement according to PDF
        :return: 
        """
        if self.current_token in (IF, ELSE):
            type_of_condition = self.current_token
            if self.current_token == IF:
                if OPEN_PARENT not in self.tokenizer.get_current_line() or CLOSED_PARENT not in \
                        self.tokenizer.get_current_line():
                    raise common.RequireSyntax(self.count_line, '( or )')
                self.tokenizer.advance()  # advancing to `(`
                self.tokenizer.advance()
                self.compileExpression()
                if self.current_token != CLOSED_PARENT:
                    raise common.RequireSyntax(self.count_line, CLOSED_PARENT)
                self.vmwriter.writeArithmetic(NOT)
                start_else_label = "L" + str(self.count_labels)
                self.count_labels += 1
                end_else_label = "L" + str(self.count_labels)
                self.count_labels += 1
                self.vmwriter.writeIf(start_else_label)  # goto else label if the condition is false
                self.compile_code_blocks()  # compiling statements
                self.vmwriter.writeGoto(end_else_label)
                self.vmwriter.writeLabel(start_else_label)
                if self.current_token == ELSE:
                    self.compile_code_blocks()
                self.vmwriter.writeLabel(end_else_label)

    def compileDo(self):
        if self.current_token == DO:
            if ';' not in self.tokenizer.get_current_line():
                raise common.RequireSyntax(self.count_line, ';')
            self.tokenizer.advance()
            self.compileTerm()
            if self.current_token == CLOSED_PARENT:
                self.tokenizer.advance()
            if self.current_token != ';':
                raise common.RequireSyntax(self.count_line, ';')
            self.tokenizer.advance()
            self.vmwriter.writePop(TEMP, 0)  # when using `do` command, the function/method probably is a void method

    def compileReturn(self):
        if self.current_token == RETURN:
            self.tokenizer.advance()
            if not self.current_token == ';':
                self.compileExpression()
            if ';' not in self.tokenizer.get_current_line() and self.current_token != ';':
                raise common.RequireSyntax(self.count_line, ';')
            self.tokenizer.advance()
            if self.subroutine_type == CONSTRUCTOR:
                self.vmwriter.writePush(POINTER, 0)
            elif self.is_subroutine_void:
                self.vmwriter.writePush(CONSTANT, 0)
            self.vmwriter.writeReturn()

    def compileExpression(self):
        """
        compiling expressions according to PDF project 10.
        we are not calling here advance method because self.compileTerm() is already doing that for us
        :return:
        """

        # while its not the end of the expression
        while self.current_token not in (OPEN_CURLY, CLOSED_CURLY, ';', CLOSED_PARENT, ']'):
            self.compileTerm()
            if self.tokenizer.symbol() == ',':
                break
            if self.current_token in OP:  # op
                arith_op = self.current_token
                self.tokenizer.advance()  # advancing to next term
                self.compileTerm()
                if arith_op == "+":
                    self.vmwriter.writeArithmetic(ADD)
                elif arith_op == "-":
                    self.vmwriter.writeArithmetic(SUB)
                elif arith_op == "*":
                    self.vmwriter.writeCall(MULTIPLY, 2)
                elif arith_op == "/":
                    self.vmwriter.writeCall(DIVISION, 2)
                elif arith_op == "<":
                    self.vmwriter.writeArithmetic(LT)
                elif arith_op == ">":
                    self.vmwriter.writeArithmetic(GT)
                elif arith_op == "&":
                    self.vmwriter.writeArithmetic(AND)
                elif arith_op == "|":
                    self.vmwriter.writeArithmetic(OR)
                elif arith_op == "=":
                    self.vmwriter.writeArithmetic(EQ)

    def compileTerm(self):
        """
        compiling term according to PDF
        :return: 
        """
        if self.current_token == "=":  # compileLet method handles this
            return self.current_token
        if self.current_token in UNARY_OP:  # if self.current == `-` or `~`
            unary_op = self.current_token
            self.tokenizer.advance()
            self.compileTerm()
            if unary_op == "~":
                self.vmwriter.writeArithmetic(NOT)
            else:
                self.vmwriter.writeArithmetic(NEG)
        elif self.tokenizer.tokenType() == KEYWORD:  # means it could be a `boolean` or `null` or `this`
            if self.current_token not in keywordConstant:
                raise common.WrongSyntax(self.count_line, self.current_token)
            self.vmwriter.writePush(CONSTANT, 0)
            if self.current_token == TRUE:
                self.vmwriter.writeArithmetic(NOT)
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == STRING_CONST:  # string constant
            self.vmwriter.writePush(CONSTANT, len(self.tokenizer.stringVal()))  # making room for string using String.new
            self.vmwriter.writeCall("String.new", 1)
            for char in self.current_token:
                self.vmwriter.writePush(CONSTANT, ord(char))
                self.vmwriter.writeCall("String.appendChar", 2)
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == INT_CONST:  # int constant
            print(self.tokenizer.get_tokens(), self.current_token, self.tokenizer.tokenType())
            self.vmwriter.writePush(CONSTANT, self.tokenizer.intVal())
            self.tokenizer.advance()
        elif self.current_token == OPEN_PARENT:
            self.tokenizer.advance()
            self.compileExpression()
            self.tokenizer.advance()
        if self.tokenizer.tokenType() == IDENTIFIER:  # function call or variable names and so on
            name = self.current_token  # name could also be name of a func/method/library and not only a variable name
            kind = self.symboltable.KindOf(name)
            index = self.symboltable.IndexOf(name)
            self.tokenizer.advance()
            if self.current_token == OPEN_PARENT:  # a method call
                self.tokenizer.advance()
                nargs = self.compileExpressionList() + 1  # +1 because of including `this`
                if self.symboltable.get_classname() not in name and THIS not in name:
                    name = self.symboltable.get_classname() + '.' + name
                self.vmwriter.writePush(POINTER, 0)
                self.vmwriter.writeCall(name, nargs)
            elif self.current_token == '.':  # if its in format of `Object/Library.method/function()`
                nargs = 0
                if OPEN_PARENT not in self.tokenizer.get_current_line() or CLOSED_PARENT not in \
                        self.tokenizer.get_current_line():
                    raise common.RequireSyntax(self.count_line, '( or )')
                self.tokenizer.advance()  # advancing to method/function name
                subroutine_name = self.current_token
                # meaning its a name of an object, which then we need to pass in `this`
                if self.symboltable.IndexOf(name) is not None:
                    kind = self.symboltable.KindOf(name)
                    name = self.symboltable.TypeOf(name)  # type of object
                    self.vmwriter.writePush(kind, 0)
                    nargs += 1
                self.tokenizer.advance()  # advancing to `(`
                self.tokenizer.advance()  # advancing to start of expressions
                nargs += self.compileExpressionList()  # also handling closing of expressionList
                self.vmwriter.writeCall(name + "." + subroutine_name, nargs)
                self.tokenizer.advance()
            else:  # if its not a subroutine call
                self.vmwriter.writePush(kind, index)
                if self.current_token == '[':  # means its array indexing
                    self.tokenizer.advance()
                    self.compileExpression()
                    if self.current_token != ']':
                        raise common.WrongSyntax(self.count_line, self.current_token)
                    self.tokenizer.advance()
                    self.vmwriter.writeArithmetic(ADD)
                    self.vmwriter.writePop(POINTER, 1)  # saving array address + index
                    self.vmwriter.writePush(THAT, 0)  # pushing value

    def compileExpressionList(self):
        """
        compiling list of expressions. list of expressions are in format like that: (expression, expressions, ...)
        usually, on other methods there are self.tokenizer.advance() line, so we would exit their part in the current
        line. here we don't need to, since self.compileExpressions() is already handling this
        :return: number of arguments user had put
        """
        expressions = self.tokenizer.get_current_line().count(',')  # how many expressions are there
        if self.tokenizer.symbol() != ')':  # if there IS an expressionList
            if CLOSED_PARENT not in self.tokenizer.get_current_line():
                raise common.RequireSyntax(self.count_line, CLOSED_PARENT)
            for _ in range(expressions + 1):
                if self.tokenizer.symbol() == ',':
                    self.tokenizer.advance()
                # print(self.tokenizer.get_tokens(), self.current_token, self.tokenizer.tokenType())
                self.compileExpression()
        else:  # if there is no an expression list
            return 0
        return expressions + 1
