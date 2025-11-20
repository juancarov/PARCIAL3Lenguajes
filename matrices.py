import sys
from antlr4 import *
from MatrixProductLexer import MatrixProductLexer
from MatrixProductParser import MatrixProductParser
from EvalMatricesVisitor import EvalMatricesVisitor

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 matrices.py archivo.txt")
        return

    input_stream = FileStream(sys.argv[1], encoding="utf-8")

    lexer = MatrixProductLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = MatrixProductParser(tokens)

    tree = parser.program()

    visitor = EvalMatricesVisitor()
    tabla = visitor.visit(tree)

    print("\nTabla final de símbolos:")
    for nombre, matriz in tabla.items():
        print(f"{nombre} = {matriz}")

if __name__ == "__main__":
    main()
