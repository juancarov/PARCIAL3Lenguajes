grammar MatrixProduct;

// --- Reglas principales ---
program
    : instruccion+ EOF
    ;

instruccion
    : declaracionMatriz
    | operacionProducto
    ;

// --- Declaración de matrices ---
declaracionMatriz
    : IDENT '=' 'MATRIX' '(' filas ')'
    ;

filas
    : fila (';' fila)*
    ;

fila
    : '[' listaValores ']'
    ;

listaValores
    : NUM (',' NUM)*
    ;

// --- Producto punto ---
operacionProducto
    : IDENT '=' 'DOTPRODUCT' '(' IDENT ',' IDENT ')'
    ;

// --- Tokens ---
NUM     : [0-9]+ ;
IDENT   : [a-zA-Z_][a-zA-Z0-9_]* ;

WS      : [ \t\r\n]+ -> skip ;
