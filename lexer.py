from typing import List, Optional

from tokens import Token, KeywordToken, TypeToken, NameTypes, TokenTypes, NameToken, OperatorToken, SyntaxToken


class Lexer:
    def __init__(self):
        self.keywords = {'class', 'extends', 'field'}
        self.types = {'int', 'float', 'str'}
        self.operators = {'='}
        self.syntax = {':', ';', '{', '}', '#'}
        self.delimiters = {'"', "'"}

        self.tokens = []

    def process_file(self, file_path):
        with open(file_path, 'r') as f:
            for line in f.readlines():
                self._process_line(line)

    def is_delimiter_close(self, char: str, previous_char: str, closing_delimiter: str):
        if previous_char == "\\":
            return False
        if char == closing_delimiter:
            return True

    def escaped(self, previous_char: str) -> bool:
        return previous_char == '\\'

    def on_keyword(self, char: str, previous_char: str, token: KeywordToken, previous_token: Token):
        self.tokens.append(token)

    def on_type(self, char: str, previous_char: str, token: TypeToken, previous_token: Token):
        self.tokens.append(token)

    def on_name(self, char: str, previous_char: str, token: NameToken, previous_token: Token):
        # Name preceded by the keyword class are new type declarations
        if previous_token.type == TokenTypes.KEYWORD and previous_token.symbol == 'class':
            token.name_type = NameTypes.CLASS
            self.types.add(token.symbol)  # Add class name as a registered type
        elif previous_token.type == TokenTypes.TYPE:
            # Field keyword appear just before the type, so 2 places before
            if self.tokens[-2].type == TokenTypes.KEYWORD and self.tokens[-2].symbol == "field":
                token.name_type = NameTypes.FIELD
        self.tokens.append(token)

    def on_operator(self, char: str, previous_char: str, token: OperatorToken, previous_token: Token):
        if self.escaped(previous_char):  # If escaped, add a name token
            self.on_name(char, previous_char, NameToken('\\' + char, NameTypes.VALUE), previous_token)
        else:  # If not, add an operator token
            self.tokens.append(token)

    def on_syntax(self, char: str, previous_char: str, token: SyntaxToken, previous_token: Token):
        if self.escaped(previous_char):
            self.on_name(char, previous_char, NameToken('\\' + char, NameTypes.VALUE), previous_token)
        else:
            self.tokens.append(token)

    def _process_line(self, line: str):
        token_buff = ''
        previous_char: Optional[str] = None
        in_delimiter: Optional[str] = None

        for char in line:
            if char == '#':
                return

            if char.isalnum() or char in '_':
                token_buff += char
            elif in_delimiter is not None and not self.is_delimiter_close(char, previous_char, in_delimiter):
                token_buff += char
            else:
                previous_token = None
                if len(self.tokens) > 0:
                    previous_token = self.tokens[-1]

                # Process one character tokens (operators, syntax and delimiters)
                if char in self.operators:
                    self.on_operator(char, previous_char, OperatorToken(char), previous_token)
                elif char in self.syntax:
                    self.on_syntax(char, previous_char, SyntaxToken(char), previous_token)
                elif char in self.delimiters:
                    if in_delimiter is None:
                        in_delimiter = char
                    else:
                        in_delimiter = None

                # Process multi characters tokens (names, types and keywords)
                if len(token_buff) > 0:
                    if token_buff in self.keywords:
                        self.on_keyword(char, previous_char, KeywordToken(token_buff), previous_token)
                    elif token_buff in self.types:
                        self.on_type(char, previous_char, TypeToken(token_buff), previous_token)
                    else:
                        self.on_name(char, previous_char, NameToken(token_buff, NameTypes.VALUE), previous_token)

                token_buff = ''
                if char.isalnum() or char == '_':
                    token_buff += char
            previous_char = char
