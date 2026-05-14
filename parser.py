class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0 

    def get_current(self):
        token = self.tokens[self.pos]
        if self.tokens[self.pos] == 'EOF': 
            return 'EOF'
        return token 
    
    def eat(self):
        if self.tokens[self.pos + 1] != 'EOF':
            self.pos += 1
        else:
            return 'EOF'
    
    def expression(self):
        result = self.term()
        while self.get_current().get('value') in ('+', '-'):
            op = self.get_current().get('value')
            self.eat()
            if op == '+':
                result += self.term()
            else:
                result -= self.term()
        return result
    

    def term(self):
        im_result = self.factor()
        while self.get_current().get('value') in ('*', '/'):
            op = self.get_current().get('value') 
            self.eat()
            if op == '*':
                im_result *= self.factor()
            else:
                div = self.factor()
                if div != 0: im_result /= div
                else: raise ZeroDivisionError('You cannot divide by zero')
        return im_result
        
    def factor(self):
        num = self.get_current().get('value')
        self.eat()
        return num