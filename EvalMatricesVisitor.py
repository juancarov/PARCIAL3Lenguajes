from MatrixProductVisitor import MatrixProductVisitor
from MatrixProductParser import MatrixProductParser

class EvalMatricesVisitor(MatrixProductVisitor):

    def __init__(self):
        self.tabla = {}   # tabla de símbolos

    # --- Declaración de matriz ---
    def visitDeclaracionMatriz(self, ctx: MatrixProductParser.DeclaracionMatrizContext):
        nombre = ctx.IDENT().getText()
        filas_ctx = ctx.filas()

        matriz = []
        for f in filas_ctx.fila():
            matriz.append(self.visit(f))

        self.tabla[nombre] = matriz
        return None

    def visitFila(self, ctx: MatrixProductParser.FilaContext):
        return [int(n.getText()) for n in ctx.listaValores().NUM()]

    # --- Operación DOTPRODUCT ---
    def visitOperacionProducto(self, ctx: MatrixProductParser.OperacionProductoContext):
        destino = ctx.IDENT(0).getText()
        Aname = ctx.IDENT(1).getText()
        Bname = ctx.IDENT(2).getText()

        if Aname not in self.tabla or Bname not in self.tabla:
            raise Exception("Error: una de las matrices no está definida.")

        A = self.tabla[Aname]
        B = self.tabla[Bname]

        # Dimensiones
        filasA = len(A)
        colsA = len(A[0])
        filasB = len(B)
        colsB = len(B[0])

        if colsA != filasB:
            raise Exception(
                f"No se puede hacer el producto: {Aname} es {filasA}x{colsA} y {Bname} es {filasB}x{colsB}"
            )

        # Producto punto
        C = []
        for i in range(filasA):
            fila = []
            for j in range(colsB):
                suma = 0
                for k in range(colsA):
                    suma += A[i][k] * B[k][j]
                fila.append(suma)
            C.append(fila)

        self.tabla[destino] = C
        return C

    # --- Programa completo ---
    def visitProgram(self, ctx: MatrixProductParser.ProgramContext):
        for inst in ctx.instruccion():
            self.visit(inst)
        return self.tabla

