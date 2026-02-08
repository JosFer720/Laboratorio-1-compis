# algoritmo shunting yard
# infix a postfix
# convierte expresiones regulares a notacion polaca inversa
class RegexConverter:
    @staticmethod
    def shunting_yard(infix):
        prec = {'*': 3, '.': 2, '|': 1, '(': 0}
        output, stack = [], []
        infix = infix.replace(" ", "")

        for c in infix:
            if c in ['L', '#']:
                output.append(c)
            elif c == '(':
                stack.append(c)
            elif c == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            else:
                while stack and prec[stack[-1]] >= prec[c]:
                    output.append(stack.pop())
                stack.append(c)

        while stack:
            output.append(stack.pop())

        return "".join(output)
