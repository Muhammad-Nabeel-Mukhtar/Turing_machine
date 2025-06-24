# lexer/lexer.py

import ply.lex as lex

# ---------------------
# Token Definitions
# ---------------------
tokens = [
    'STATE',
    'SYMBOL',
    'ARROW',
    'DIRECTION'
]

# Fixed symbol tokens
t_ARROW = r'->'
t_DIRECTION = r'R|L|S'

# Dynamic token patterns
def t_STATE(t):
    r'q[0-9H]+'
    return t

def t_SYMBOL(t):
    r'[01_]'
    return t

# Ignore whitespace and tabs
t_ignore = ' \t'

# Ignore comments (starting with #)
def t_COMMENT(t):
    r'\#.*'
    pass

# Track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handler
def t_error(t):
    print(f"[Lexer Error] Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()


# ---------------------
# Main entry (for testing)
# ---------------------
if __name__ == "__main__":
    lexer = lex.lex()
    try:
        with open("input/config.tm", "r") as file:
            data = file.read()
            lexer.input(data)
            print("=== TOKENS ===")
            for token in lexer:
                print(token)
    except FileNotFoundError:
        print("Error: config.tm not found. Please ensure it exists in /input/")
