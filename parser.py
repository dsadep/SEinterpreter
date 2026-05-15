class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0 

    def get_current(self):
        token = self.tokens[self.pos]
        if self.tokens[self.pos] == 'EOF': 
            return 'EOF'
        return token.get('value')
    
    def eat(self):
        if self.tokens[self.pos + 1] != 'EOF':
            self.pos += 1
        else:
            return 'EOF'
    
    def evaluate(self):
        result = self.expression()
        if self.get_current() != 'EOF':
            raise SyntaxError('Unexpected )')
        return result


    def expression(self):
        result = self.term()
        while self.get_current() in ('+', '-'):
            op = self.get_current()
            self.eat()
            if op == '+':
                result += self.term()
            else:
                result -= self.term()

        return result
    

    def term(self):
        im_result = self.factor()
        while self.get_current() in ('*', '/'):
            op = self.get_current()
            self.eat()
            if op == '*':
                im_result *= self.factor()
            elif op == '/':
                div = self.factor()
                if div != 0: im_result /= div
                else: raise ZeroDivisionError('You cannot divide by zero')
            else: 
                self.factor()
        return im_result
        
    def factor(self):
        num = self.get_current()
        if isinstance(num, int):
            self.eat()
            return num
        elif num == '(':
            self.eat()
            brackets_result = self.expression()
            if brackets_result == None:
                raise SyntaxError('Empty brackets are not supporting right now')
            if self.get_current() != ')':
                raise SyntaxError('Expected )')
            self.eat()
            return brackets_result 