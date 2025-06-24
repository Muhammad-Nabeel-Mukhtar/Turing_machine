import streamlit as st
import os
import shutil

# Custom modules
from parser import parser
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
        # Parse and analyze
        parser.parse_tm_config(CONFIG_PATH)
        generate_tm_graph(parser.transitions)

        # Run simulation
        output = run_turing_machine(user_input, parser.transitions)

        st.success("✅ Simulation Complete!")
        st.subheader("🧾 Final Tape Output:")
        st.code(output, language="text")

        # Show CFG graph
        if os.path.exists(GRAPH_PATH):
            st.subheader("📊 AST / CFG Visualization")
            st.image(GRAPH_PATH, caption="Transition Graph", use_column_width=True)
