import graphviz
import os

def generate_tm_graph(transitions, output_path="output/tm_cfg_ast.png"):
    dot = graphviz.Digraph(comment="Turing Machine CFG/AST")

    # Add all states as nodes
    states = set(t["current_state"] for t in transitions).union(
        t["next_state"] for t in transitions)
    for state in states:
        shape = "doublecircle" if state.lower() == "qh" else "circle"
        dot.node(state, shape=shape)

    # Add edges with labels
    for t in transitions:
        label = f"{t['read_symbol']}→{t['write_symbol']},{t['direction']}"
        dot.edge(t["current_state"], t["next_state"], label=label)

    # Render as PNG
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    dot.render(output_path, format="png", cleanup=True)
