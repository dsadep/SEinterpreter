signs = ('+', '-', '*', '/')

class Converter:
    @staticmethod 
    def convert(expression: list):
        result = []
        i = 0
        while i < len(expression):
            if expression[i] != ' ':
                try: 
                    result.append(int(expression[i]))
                except ValueError as error: 
                    if expression[i] not in signs:
                        raise error
                    result.append(expression[i])
            i += 1
        result.append('EOF')
        return result