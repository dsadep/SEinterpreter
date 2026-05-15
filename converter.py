signs = {'+', '-', '*', '/', '(', ')'}

class Converter:
    @staticmethod 
    def convert(expression: list):
        result = []
        i = 0
        while i < len(expression):
            if expression[i] != ' ':
                if expression[i] in signs:
                    result.append(expression[i])
                    i += 1

                elif expression[i].isdigit():
                    end = Converter.parse_number(i, expression)
                    number = int(expression[i:end])
                    result.append(number)
                    i += len(str(number))
                else:
                    print('unexpectedf character: {}'.format(expression[i]))
                    i+=1
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