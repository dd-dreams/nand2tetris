
# keywords
IF = "if"
ELSE = "else"
CLASS = "class"
CONSTRUCTOR = "constructor"
FUNCTION = "function"
METHOD = "method"
FIELD = "field"
STATIC = "static"
VAR = "var"
TRUE = "true"
FALSE = "false"
NULL = "null"
THIS = "this"
LET = "let"
DO = "do"
WHILE = "while"
RETURN = "return"
INT = "int"
BOOLEAN = "boolean"
CHAR = "char"
VOID = "void"
OPEN_CURLY = '{'
CLOSED_CURLY = '}'
OPEN_PARENT = '('
CLOSED_PARENT = ')'
ARRAY = "Array"
TYPES = [CHAR, INT, BOOLEAN, VOID, ARRAY]
OP = ['+', '-', '*', '/', '/', '&', '|', '<', '>', '=']
UNARY_OP = ['-', '~']
keywordConstant = [TRUE, FALSE, NULL, THIS]
KEYWORDS = [IF, ELSE, CLASS, CONSTRUCTOR, FUNCTION, METHOD, FIELD, STATIC, VAR, TRUE, FALSE, NULL, THIS, LET, DO,
            WHILE, RETURN, INT, BOOLEAN, CHAR, VOID]

KEYWORD = "keyword"
SYMBOL = "symbol"
IDENTIFIER = "identifier"
INT_CONST = "integerConstant"
STRING_CONST = "stringConstant"


ARG = "argument"
LOCAL = "local"
CONSTANT = "constant"
POINTER = "pointer"
TEMP = "temp"
THIS = "this"
THAT = "that"


# VM commands
PUSH = "push "
POP = "pop "
RETURN = "return"
LABEL = "label "
GOTO = "goto "
IF_GOTO = "if-goto "
CALL = "call "
FUNCTION_VM = "function "
ADD = "add"
SUB = "sub"
NEG = "neg"
EQ = "eq"
GT = "gt"
LT = "lt"
AND = "and"
OR = "or"
NOT = "not"
MULTIPLY = "Math.multiply"
SQRT = "Math.sqrt"
DIVISION = "Math.divide"

RE_MATCH_TOKENS = r"[\[\]{}().,*/\|<>+_\-;=\&\~]|\"[\w\s?,;:]+|\w+"
