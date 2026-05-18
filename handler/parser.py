from ast_nodes import AssignNode, NumberNode, UnaryOpNode, BinaryOpNode, VarNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def get_current(self):
        token = self.tokens[self.pos].get('value')
        if token == 'EOF':
            return 'EOF'
        return token

    def eat(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1

    def program(self):
        result = self.statement()
        if self.get_current() != 'EOF':
            raise SyntaxError('Unexpected token')
        return result

    def statement(self):
        return self.assignment()

    def assignment(self):
        name = self.get_current()
        if self.tokens[self.pos].get('type') == 'VAR':
            if self.tokens[self.pos + 1].get('type') == 'ASSIGN':
                self.eat() 
                self.eat()
                value = self.expression()
                return AssignNode(name, value)
        name = self.expression()            
        return name

    def expression(self):
        result = self.logical_or()
        return result

    def logical_or(self):
        result = self.logical_and()
        while self.get_current() == 'or':
            self.eat()
            result = BinaryOpNode(result, 'or', self.logical_and())
        return result

    def logical_and(self):
        result = self.equality()
        while self.get_current() == 'and':
            self.eat()
            result = BinaryOpNode(result, 'and', self.equality())
        return result

    def equality(self):
        left = self.comparison()
        while self.get_current() in ('!=', '=='):
            op = self.get_current()
            self.eat()
            if op == '==':
                left = BinaryOpNode(left, '==', self.comparison())
            else:
                left = BinaryOpNode(left, '!=', self.comparison())
        return left


    def comparison(self):
        left = self.additive()
        while self.get_current() in ('>=', '<=', '>', '<'):
            op = self.get_current()
            self.eat()
            if op == '>=':
                left = BinaryOpNode(left, '>=', self.additive())
            elif op == '>':
                left = BinaryOpNode(left, '>', self.additive())
            elif op == '<=':
                left = BinaryOpNode(left, '<=', self.additive())
            else:
                left = BinaryOpNode(left, '<', self.additive())
        return left

    def additive(self):
        result = self.multiplicative()
        while self.get_current() in ('+', '-'):
            op = self.get_current()
            self.eat()
            if op == '+':
                result = BinaryOpNode(result, '+', self.multiplicative())
            else:
                result = BinaryOpNode(result, '-', self.multiplicative())
        return result

    def multiplicative(self):
        im_result = self.unary()
        while self.get_current() in ('*', '/'):
            op = self.get_current()
            self.eat()
            if op == '*':
                im_result = BinaryOpNode(im_result, '*', self.unary())
            elif op == '/':
                im_result = BinaryOpNode(im_result, '/', self.unary())
        return im_result

    def unary(self):
        while self.get_current() in ('-', '+'):
            un = self.get_current()
            self.eat()
            if un == '-':
                result = UnaryOpNode('-', self.unary())
            else:
                result = UnaryOpNode('+', self.unary())
            return result
        return self.power()

    def power(self):
        left = self.factor()
        if self.get_current() == '^':
            self.eat()
            result = BinaryOpNode(left, '^', self.unary())
            return result
        return left

    def factor(self):
        num = self.get_current()
        if isinstance(num, int):
            self.eat()
            return NumberNode(num)
        elif num == '(':
            self.eat()
            brackets_result = self.logical_or()
            if brackets_result == None:
                raise SyntaxError('Empty brackets are not supporting right now')
            if self.get_current() != ')':
                raise SyntaxError('Expected )')
            self.eat()
            return brackets_result
        elif self.tokens[self.pos].get('type') == 'VAR':
            self.eat()
            return VarNode(num)