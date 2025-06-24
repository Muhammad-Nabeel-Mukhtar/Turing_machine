# visualizer/ast_cfg_visualizer.py
import graphviz
import streamlit as st  # Streamlit renderer

def generate_tm_graph(transitions):
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')

    # Add states as nodes
    states = set()
    for t in transitions:
        states.add(t['current_state'])
        states.add(t['next_state'])

    for state in states:
        shape = 'doublecircle' if state.lower() in ['qh', 'halt'] else 'circle'
        dot.node(state, shape=shape)

    # Add transitions as edges
    for t in transitions:
        label = f"{t['read_symbol']}→{t['write_symbol']},{t['direction']}"
        dot.edge(t['current_state'], t['next_state'], label=label)

    # Render in Streamlit
    st.graphviz_chart(dot)
