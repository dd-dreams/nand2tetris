
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
TYPES = [CHAR, INT, BOOLEAN, VOID]
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


RE_MATCH_TOKENS = r"[\[\]{}().,*/\|<>+_\-;=\&\~]|\"[\w\s]+\"|\w+"
