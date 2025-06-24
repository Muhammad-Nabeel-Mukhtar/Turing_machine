import streamlit as st
import os
import shutil

# Custom modules
from tm_parser.tm_parser import parse_tm_config
from visualizer.ast_cfg_visualizer import generate_tm_graph
from tm_engine.simulator import run_turing_machine

# Paths
CONFIG_PATH = "input/config.tm"
GRAPH_PATH = "output/tm_cfg_ast.png"

# Page settings
st.set_page_config(page_title="Turing Machine Simulator", layout="centered")
st.title("🧠 Turing Machine Simulator")
st.markdown("Simulate a Turing Machine using custom `.tm` configuration and binary input.")

# --- Upload Config File ---
st.subheader("1. Upload `.tm` Configuration File")

uploaded_file = st.file_uploader("Upload your config.tm file", type=["tm"])
if uploaded_file:
    os.makedirs("input", exist_ok=True)
    with open(CONFIG_PATH, "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ Configuration file uploaded.")

# --- Input Binary String ---
st.subheader("2. Enter Binary Input for Simulation")

user_input = st.text_input("Binary input (e.g., 1011):")
if user_input and not all(c in '01' for c in user_input):
    st.error("❌ Input must be binary (0 and 1 only).")

# --- Process and Run Simulation ---
if st.button("🚀 Run Turing Machine"):
    if not os.path.exists(CONFIG_PATH):
        st.warning("Please upload a `.tm` configuration file.")
    elif not user_input:
        st.warning("Please enter a binary string.")
    elif not all(c in '01' for c in user_input):
        st.error("Invalid input: only binary digits allowed.")
    else:
        transitions = parse_tm_config(CONFIG_PATH)
        if not transitions:
            st.error("❌ Failed to parse config file.")
        else:
            # Visualize CFG/AST
            with st.expander("📊 View Transition Graph"):
                try:
                    generate_tm_graph(transitions)
                    if os.path.exists(GRAPH_PATH):
                        st.image(GRAPH_PATH, caption="Transition Graph", use_column_width=True)
                except Exception as e:
                    st.warning(f"[Graphviz Error] Could not generate graph: {e}")

            # Run Turing Machine
            output = run_turing_machine(transitions, user_input)

            st.success("✅ Simulation Complete!")
            st.subheader("🧾 Final Tape Output:")
            st.code(output, language="text")
