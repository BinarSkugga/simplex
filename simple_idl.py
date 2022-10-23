from pprint import pprint
from typing import List

from lexer import Lexer
from tokens import TokenTypes, NameTypes, Token


class Parser:
    def __init__(self):
        pass

    def generate_dict(self, tokens: List[Token]):
        tree = {t: {'index': i} for i, t in enumerate(tokens)
                if t.type == TokenTypes.NAME and t.name_type == NameTypes.CLASS}

        for class_token, sub_tree in tree.items():
            class_tokens = []

            in_class = False
            for t in tokens[sub_tree['index']:]:
                if t.type == TokenTypes.SYNTAX and t.symbol == '{':
                    in_class = True
                    continue
                if t.type == TokenTypes.SYNTAX and t.symbol == '}':
                    break
                if in_class:
                    class_tokens.append(t)
            sub_tree['tokens'] = class_tokens

        for class_token, sub_tree in tree.items():
            sub_tree['fields'] = []
            curr_line = []
            is_field = False
            for t in sub_tree['tokens']:
                if t.type == TokenTypes.SYNTAX and t.symbol == ';':
                    sub_tree['fields'].append(curr_line)
                    curr_line = []
                    is_field = False
                if t.type == TokenTypes.KEYWORD and t.symbol == 'field':
                    is_field = True
                    continue
                if is_field:
                    curr_line.append(t)
            del sub_tree['tokens']
        return tree


lexer = Lexer()
lexer.process_file('simple_class.simp')

print(lexer.tokens)

parser = Parser()
pprint(parser.generate_dict(lexer.tokens))
