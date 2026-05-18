from ast_nodes import AssignNode, NumberNode, UnaryOpNode, BinaryOpNode, VarNode

class Evaluator:
    def __init__(self):
        self.vars = {}

    def eval(self, node):
        if isinstance(node, NumberNode):
            return node.value
        
        if isinstance(node, UnaryOpNode):
            value = self.eval(node.operand)

            if node.op == '-':
                return -value
            if node.op == '+':
                return +value
            
            raise ValueError('Unknow unary operator {}'.format(node.op))
        
        if isinstance(node, BinaryOpNode):
            left = self.eval(node.left)
            right = self.eval(node.right)

            if node.op == '+':
                return left + right
            if node.op == '-':
                return left - right 
            if node.op == '*':
                return left * right
            if node.op == '/':
                if right == 0:
                    raise ZeroDivisionError('You cannot divide by zero')
                return left / right 
            if node.op == '^':
                return left ** right
            
            if node.op == '==':
                return left == right
            if node.op == '!=':
                return left != right
            if node.op == '>':
                return left > right
            if node.op == '<':
                return left < right
            if node.op =='>=':
                return left >= right
            if node.op == '<=':
                return left <= right
            
            if node.op == 'and':
                return left and right
            if node.op == 'or':
                return left or right
        
        if isinstance(node, VarNode):
            if node.name in self.vars:
                return self.vars[node.name]
            raise ValueError('No value')
        
        if isinstance(node, AssignNode):
            value = self.eval(node.value)
            self.vars[node.name] = value
        else:
            raise ValueError('Unknown operator {}'.format(node.op))