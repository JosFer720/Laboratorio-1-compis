# palabras reservadas del lenguaje
KEYWORDS = {
    "public", "class", "private", "static", "final",
    "double", "int", "void", "new", "return"
}

# clase que representa un token
class Token:
    # constructor del token
    def __init__(self, tipo, valor, pos):
        self.tipo = tipo
        self.valor = valor
        self.pos = pos

    # representacion en texto del token
    def __repr__(self):
        return f"<{self.tipo}, {self.pos}>"

# clase principal del analizador lexico
class AnalizadorLexico:
    # inicializa el analizador con el codigo fuente
    def __init__(self, source_code):
        self.code = source_code
        self.lexemeBegin = 0
        self.forward = 0
        self.pos = 0

    # metodo para obtener el siguiente token
    def siguiente_token(self):
        n = len(self.code)

        # saltar espacios en blanco
        while self.forward < n and self.code[self.forward].isspace():
            self.forward += 1
            self.lexemeBegin = self.forward

        if self.forward >= n:
            return None

        c = self.code[self.forward]

        # identificadores
        if c.isalpha() or c == '_':
            self.forward += 1
            while self.forward < n and (
                self.code[self.forward].isalnum() or self.code[self.forward] == '_'
            ):
                self.forward += 1

            lexema = self.code[self.lexemeBegin:self.forward]
            tipo = "KEYWORD" if lexema in KEYWORDS else "ID"
            token = Token(tipo, lexema, self.pos)
            self.pos += 1
            self.lexemeBegin = self.forward
            return token

        # numeros
        if c.isdigit():
            self.forward += 1
            while self.forward < n and self.code[self.forward].isdigit():
                self.forward += 1

            token = Token("NUMBER", None, self.pos)
            self.pos += 1
            self.lexemeBegin = self.forward
            return token

        # cadenas de texto
        if c == '"':
            self.forward += 1
            while self.forward < n and self.code[self.forward] != '"':
                self.forward += 1
            self.forward += 1

            token = Token("STRING", None, self.pos)
            self.pos += 1
            self.lexemeBegin = self.forward
            return token

        # operadores
        if c in "+-*/=<>!":
            self.forward += 1
            token = Token("OPERATOR", None, self.pos)
            self.pos += 1
            self.lexemeBegin = self.forward
            return token

        # simbolos
        if c in "{}();,.":
            self.forward += 1
            token = Token("SYMBOL", None, self.pos)
            self.pos += 1
            self.lexemeBegin = self.forward
            return token

        # desconocido
        self.forward += 1
        token = Token("UNKNOWN", None, self.pos)
        self.pos += 1
        self.lexemeBegin = self.forward
        return token
