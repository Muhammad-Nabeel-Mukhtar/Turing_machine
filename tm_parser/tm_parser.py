# tm_parser/tm_parser.py

import sys
sys.path.insert(0, '.')

import ply.yacc as yacc
from lexer.lexer import tokens  # Reuse tokens from lexer.py

transitions = []

def p_statements_multiple(p):
    '''statements : statements statement'''
    pass

def p_statements_single(p):
    '''statements : statement'''
    pass

def p_statement(p):
    '''statement : STATE SYMBOL ARROW STATE SYMBOL DIRECTION'''
    transition = {
        'current_state': p[1],
        'read_symbol': p[2],
        'next_state': p[4],
        'write_symbol': p[5],
        'direction': p[6]
    }
    transitions.append(transition)

def p_error(p):
    if p:
        print(f"[Parser Error] Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("[Parser Error] Unexpected end of input")

def parse_tm_config(filepath):
    import lexer.lexer as lexer_module
    global transitions
    transitions = []

    lexer = lexer_module.lexer
    parser = yacc.yacc()

    try:
        with open(filepath, "r") as file:
            data = file.read()
            parser.parse(data, lexer=lexer)
            print("=== PARSED TRANSITIONS ===")
            for t in transitions:
                print(t)

            from semantic.semantic import check_semantics
            check_semantics(transitions)
            return transitions  # ✅ Return transitions here

    except FileNotFoundError:
        print(f"[Error] Config file not found: {filepath}")
        return []

