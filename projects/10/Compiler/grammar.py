from constants import SYMBOL, KEYWORD


def is_symbol(token):
    symbols_ = {'{',
                '}',
                '(',
                ')',
                '[',
                ']',
                '.',
                ',',
                ';',
                '+',
                '-',
                '*',
                '/',
                '&',
                '|',
                '<',
                '>',
                '=',
                '-',
                '~'}
    if token in symbols_:
        return SYMBOL


def integerConstant(num):
    if num.isdigit() and 0 <= int(num) <= 32767:
        return True
    return False
