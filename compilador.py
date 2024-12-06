import re

# Definição dos padrões de tokens conforme a gramática da linguagem LPD
TOKEN_PATTERNS = {
    'COMMENT': r'\{.*?\}',                   # Comentários delimitados por { }
    'RESERVED': r'\b(program|int|char|float|if|then|else|while|do|repeat|until|begin|end|readd|readc|writed|writec|div|or|and|not)\b',
    'IDENTIFIER': r'\b[a-zA-Z][a-zA-Z0-9_]*\b',  # Identificadores válidos
    'NUMBER': r'\b\d+\b',                   # Números inteiros
    'CHAR_LITERAL': r"'(.)'",              # Literais de caracteres entre aspas simples
    'ASSIGN': r':=',                        # Operador de atribuição
    'REL_OP': r'[<>]=?|<>|=',               # Operadores relacionais
    'ARITH_OP': r'[+\-*/]',                 # Operadores aritméticos
    'PUNCTUATION': r'[;,\[\]\(\)\.]',       # Símbolos de pontuação
    'WHITESPACE': r'\s+',                   # Espaços em branco (ignorados)
}

def tokenize(code):
    """
    Analisador léxico para a linguagem LPD.
    Lê o código-fonte e gera uma lista de tokens.

    Parâmetros:
    code (str): O código-fonte da linguagem LPD.

    Retorno:
    list: Lista de dicionários contendo os tokens encontrados.

    Cada token possui:
    - atom: A sequência de caracteres do token.
    - symbol: O tipo do token.
    - line: O número da linha onde o token foi encontrado.
    """
    token_list = []
    line_number = 1

    for line in code.splitlines():
        index = 0
        while index < len(line):
            match = None
            for token_type, pattern in TOKEN_PATTERNS.items():
                regex = re.compile(pattern)
                match = regex.match(line, index)
                if match:
                    # Ignora comentários e espaços em branco
                    if token_type != 'WHITESPACE' and token_type != 'COMMENT':
                        token_list.append({
                            'atom': match.group(),
                            'symbol': token_type,
                            'line': line_number
                        })
                    index = match.end()
                    break
            if not match:
                raise ValueError(f"Token inválido na linha {line_number}: {line[index]}")
        line_number += 1

    return token_list

# Exemplo de código para teste
code = """
program Logica;
var int a, b;
begin
    a := 10;
    b := 20;
    if (a < b) and (b > 15) then
        writed(a + b);
    if not (a = b) then
        writed(b - a);
end.
"""

# Execução do analisador léxico
tokens = tokenize(code)
for token in tokens:
    print(token)
