from enum import IntEnum
from typing import Optional


class TokenTypes(IntEnum):
    LINE_START = 0
    KEYWORD = 1
    TYPE = 2
    OPERATOR = 3
    SYNTAX = 4
    NAME = 5


class NameTypes(IntEnum):
    CLASS = 1
    FIELD = 2
    VALUE = 3


class Token:
    def __init__(self, symbol: Optional[str], _type: TokenTypes):
        self.symbol = symbol
        self.type = _type


class KeywordToken(Token):
    def __init__(self, symbol: Optional[str]):
        super().__init__(symbol, TokenTypes.KEYWORD)

    def __repr__(self):
        return f'{self.symbol}'


class TypeToken(Token):
    def __init__(self, symbol: Optional[str]):
        super().__init__(symbol, TokenTypes.TYPE)

    def __repr__(self):
        return f'type({self.symbol})'


class OperatorToken(Token):
    def __init__(self, symbol: Optional[str]):
        super().__init__(symbol, TokenTypes.OPERATOR)

    def __repr__(self):
        return f'{self.symbol}'


class SyntaxToken(Token):
    def __init__(self, symbol: Optional[str]):
        super().__init__(symbol, TokenTypes.SYNTAX)


class NameToken(Token):
    def __init__(self, symbol: Optional[str], name_type: NameTypes):
        super().__init__(symbol, TokenTypes.NAME)
        self.name_type = name_type

    def __repr__(self):
        return f'{self.name_type.name}({self.symbol})'
