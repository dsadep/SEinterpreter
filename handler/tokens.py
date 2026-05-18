default_dict = {
    '+': 'ADD',
    '-': 'SUB',
    '*': 'MUL',
    '/': 'DIV',
    '(': 'LPAREN',
    ')': 'RPAREN',
    '^': 'POWER',
    'or': 'OR',
    'and': 'AND',
    '>=': 'GE',
    '<=': 'LE',
    '>': 'GT',
    '<': 'LT',
    '==': 'EQ',
    '!=': 'NEQ',
    '=': 'ASSIGN'
}

class Tokeniser:
    @staticmethod
    def tokenise(splitted_expression):
        tokens = []
        for item in splitted_expression:
            tok = {}
            tok['type'] = None
            tok['value'] = item
            if item in default_dict.keys():
                tok['type'] = default_dict.get(item)
            elif item == 'EOF':
                tok['type'] = 'EOF'
            elif isinstance(item, int): 
                tok['type'] = 'NUM'
            else:
                tok['type'] = 'VAR'
            tokens.append(tok)
        return tokens