signs = {'+', '-', '*', '/', '(', ')', '^'}
words = {'and', 'or'}
comparison_signs = {'>', '<', '=', '!'}
comparison_operands = {'>', '<', '==', '!=', '>=', '<='}
assign = '='

class UnexpectedCharacter(BaseException):
    pass

class Converter:
    @staticmethod 
    def convert(expression: list):
        result = []
        i = 0
        while i < len(expression):
            current = expression[i]
            if current != ' ':
                if current in signs:
                    result.append(current)
                    i += 1

                elif current.isdigit():
                    end = Converter.parse_number(i, expression)
                    number = int(expression[i:end])
                    result.append(number)
                    i += len(str(number))

                elif current.isalpha():
                    end = Converter.parse_word(i, expression)
                    word = expression[i:end].lower()
                    result.append(word)
                    i += len(word)
                
                elif current in comparison_signs:
                    end = Converter.parse_operand(i, expression)
                    operand = expression[i:i+2] if end != i else current
                    if operand in comparison_operands:
                        result.append(operand)
                        i += len(operand)
                    elif operand == assign:
                        result.append(operand)
                        i += 1 
                    else: raise SyntaxError('Unsupported operand')

                else:
                    raise SyntaxError('unexpectedf character: {}. expression cannot be calculated'.format(expression[i]))
            else:
                i += 1
        result.append('EOF')
        return result
    
    @staticmethod
    def parse_number(start, expression):
        end = start
        while end  < len(expression):
            if expression[end].isdigit():
                end += 1
            else:
                break
        return end
    
    @staticmethod
    def parse_word(start, expression):
        end = start
        while end  < len(expression):
            if expression[end].isalpha():
                end += 1
            else:
                break
        return end
    
    @staticmethod
    def parse_operand(start, expression):
        if expression[start:start+2] in comparison_operands:
            return start + 1
        return start