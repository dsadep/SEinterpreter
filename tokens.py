default_dict = {
    '+': 'ADD',
    '-': 'SUB',
    '*': 'MUL',
    '/': 'DIV',
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
            else: 
                tok['type'] = 'NUM'
            tokens.append(tok)
        return tokens