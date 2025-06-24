import os
from graphviz import Digraph

# This function creates a visualization of the Turing Machine transitions as a control flow graph (CFG-style)
def generate_tm_graph(transitions, output_path='output/tm_ast_cfg'):
    dot = Digraph(comment='Turing Machine CFG')

    # Create nodes for states
    states = set(t['current_state'] for t in transitions)
    states.update(t['next_state'] for t in transitions)
    for state in states:
        shape = 'doublecircle' if state.startswith('qH') else 'circle'
        dot.node(state, state, shape=shape)

    # Create edges for transitions
    for t in transitions:
        label = f"{t['read_symbol']} → {t['write_symbol']}, {t['direction']}"
        dot.edge(t['current_state'], t['next_state'], label=label)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save and render
    dot.render(output_path, format='png', cleanup=True)
    print(f"[+] Graphviz AST/CFG saved to {output_path}.png")


# If running directly for testing
if __name__ == '__main__':
    # Example transitions (you can replace this with parser output)
    transitions = [
        {'current_state': 'q0', 'read_symbol': '1', 'next_state': 'q0', 'write_symbol': '1', 'direction': 'R'},
        {'current_state': 'q0', 'read_symbol': '0', 'next_state': 'q0', 'write_symbol': '0', 'direction': 'R'},
        {'current_state': 'q0', 'read_symbol': '_', 'next_state': 'q1', 'write_symbol': '_', 'direction': 'L'},
        {'current_state': 'q1', 'read_symbol': '1', 'next_state': 'q1', 'write_symbol': '0', 'direction': 'L'},
        {'current_state': 'q1', 'read_symbol': '0', 'next_state': 'q2', 'write_symbol': '1', 'direction': 'S'},
        {'current_state': 'q1', 'read_symbol': '_', 'next_state': 'q2', 'write_symbol': '1', 'direction': 'S'},
        {'current_state': 'q2', 'read_symbol': '1', 'next_state': 'q2', 'write_symbol': '1', 'direction': 'S'},
        {'current_state': 'q2', 'read_symbol': '0', 'next_state': 'q2', 'write_symbol': '0', 'direction': 'S'},
        {'current_state': 'q2', 'read_symbol': '_', 'next_state': 'qH', 'write_symbol': '_', 'direction': 'S'},
    ]

    generate_tm_graph(transitions)
