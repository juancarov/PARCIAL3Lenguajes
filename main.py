import re

# ============================================
# LEXER
# ============================================

TOKEN_REGEX = [
    ("CREAR", r"CREAR"),
    ("TABLA", r"TABLA"),
    ("INSERTAR", r"INSERTAR"),
    ("EN", r"EN"),
    ("VALORES", r"VALORES"),
    ("LEER", r"LEER"),
    ("DE", r"DE"),
    ("DONDE", r"DONDE"),
    ("ACTUALIZAR", r"ACTUALIZAR"),
    ("COLOCAR", r"COLOCAR"),
    ("ELIMINAR", r"ELIMINAR"),

    ("NUM", r"[0-9]+"),
    ("TEXTO", r"\"[^\"]*\""),
    ("IDENT", r"[a-zA-Z_][a-zA-Z0-9_]*"),

    ("COMA", r","),
    ("PARI", r"\("),
    ("PARD", r"\)"),
    ("IGUAL", r"="),

    ("WS", r"[ \t\r\n]+"),
]

def lexer(input_text):
    tokens = []
    i = 0

    while i < len(input_text):
        match = None

        for token_type, pattern in TOKEN_REGEX:
            regex = re.compile(pattern)
            match = regex.match(input_text, i)

            if match:
                lexema = match.group(0)

                if token_type != "WS":
                    tokens.append((token_type, lexema))

                i = match.end(0)
                break

        if not match:
            raise Exception(f"Token inválido: {input_text[i]}")

    tokens.append(("EOF", "EOF"))
    return tokens


# ============================================
# PARSER RECURSIVO DESCENDENTE
# ============================================

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.tabla_simbolos = {}

    def current(self):
        return self.tokens[self.pos]

    def eat(self, token_type):
        tipo, lex = self.current()
        if tipo == token_type:
            self.pos += 1
            return lex
        raise Exception(f"Se esperaba {token_type} y llegó {tipo}")

    # ------------------------------
    # PROGRAMA
    # ------------------------------

    def programa(self):
        traducciones = []

        while self.current()[0] != "EOF":
            traducciones.append(self.operacionCrud())

        return traducciones, self.tabla_simbolos

    def operacionCrud(self):
        tipo = self.current()[0]

        if tipo == "CREAR":
            return self.crearTabla()

        if tipo == "INSERTAR":
            return self.insertarFila()

        if tipo == "LEER":
            return self.leerDatos()

        if tipo == "ACTUALIZAR":
            return self.actualizarDatos()

        if tipo == "ELIMINAR":
            return self.eliminarDatos()

        raise Exception("Operación CRUD no reconocida")

    # ---------------------------------------------------
    # CREAR
    # ---------------------------------------------------

    def crearTabla(self):
        self.eat("CREAR")
        self.eat("TABLA")
        nombre = self.eat("IDENT")

        self.tabla_simbolos[nombre] = {"columnas": []}

        return f"create({nombre})"

    # ---------------------------------------------------
    # INSERTAR FILA
    # ---------------------------------------------------

    def insertarFila(self):
        self.eat("INSERTAR")
        self.eat("EN")
        nombre = self.eat("IDENT")

        self.eat("VALORES")
        self.eat("PARI")
        valores = self.listaValores()
        self.eat("PARD")

        # Si la tabla no existe, crearla
        if nombre not in self.tabla_simbolos:
            self.tabla_simbolos[nombre] = {"columnas": []}

        # Si no hay columnas definidas aún, deducirlas:
        if not self.tabla_simbolos[nombre]["columnas"]:
            columnas = []
            for i in range(len(valores)):
                columnas.append(f"col{i+1}")
            self.tabla_simbolos[nombre]["columnas"] = columnas

        return f"insert({nombre}, [{', '.join(valores)}])"

    def listaValores(self):
        valores = [self.valor()]
        while self.current()[0] == "COMA":
            self.eat("COMA")
            valores.append(self.valor())
        return valores

    # ---------------------------------------------------
    # LEER
    # ---------------------------------------------------

    def leerDatos(self):
        self.eat("LEER")
        self.eat("DE")
        nombre = self.eat("IDENT")

        if self.current()[0] == "DONDE":
            self.eat("DONDE")
            cond = self.condicion()
            return f"read({nombre}, {cond})"

        return f"read({nombre})"

    def condicion(self):
        campo = self.eat("IDENT")
        self.eat("IGUAL")
        val = self.valor()
        return f"cond({campo}, '=', {val})"

    # ---------------------------------------------------
    # ACTUALIZAR
    # ---------------------------------------------------

    def actualizarDatos(self):
        self.eat("ACTUALIZAR")
        nombre = self.eat("IDENT")
        self.eat("COLOCAR")

        asignaciones = self.listaAsignaciones()
        texto = ",".join(asignaciones)

        return f"update({nombre}, {{{texto}}})"

    def listaAsignaciones(self):
        asign = [self.asignacion()]
        while self.current()[0] == "COMA":
            self.eat("COMA")
            asign.append(self.asignacion())
        return asign

    def asignacion(self):
        campo = self.eat("IDENT")
        self.eat("IGUAL")
        val = self.valor()
        return f"{campo}={val}"

    # ---------------------------------------------------
    # ELIMINAR
    # ---------------------------------------------------

    def eliminarDatos(self):
        self.eat("ELIMINAR")
        self.eat("DE")
        nombre = self.eat("IDENT")

        if self.current()[0] == "DONDE":
            self.eat("DONDE")
            cond = self.condicion()
            return f"delete({nombre}, {cond})"

        return f"delete({nombre})"

    # ---------------------------------------------------
    # VALOR
    # ---------------------------------------------------

    def valor(self):
        tipo, lex = self.current()

        if tipo == "TEXTO":
            self.eat("TEXTO")
            return lex

        if tipo == "NUM":
            self.eat("NUM")
            return lex

        raise Exception("Valor inválido")


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    entrada = input("Ingrese consulta CRUD: ")

    tokens = lexer(entrada)
    parser = Parser(tokens)

    traducciones, tabla = parser.programa()

    print("\n--- Traducción (gramática de atributos) ---")
    for t in traducciones:
        print(t)

    print("\n--- Tabla de símbolos ---")
    for k, v in tabla.items():
        print(k, ":", v)

