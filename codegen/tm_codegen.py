from llvmlite import ir
import os
import json

# Load transitions from parsed output
with open("output/transitions.json", "r") as f:
    transitions = json.load(f)

def codegen_turing_machine(transitions):
    # Create LLVM module and builder
    module = ir.Module(name="turing_machine")
    func_type = ir.FunctionType(ir.VoidType(), [], False)
    func = ir.Function(module, func_type, name="main")
    block = func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    # Define data types
    int8 = ir.IntType(8)
    int32 = ir.IntType(32)

    # Tape: 300 cells of int8
    tape_type = ir.ArrayType(int8, 300)
    tape = builder.alloca(tape_type, name="tape")
    head = builder.alloca(int32, name="head")
    builder.store(ir.Constant(int32, 100), head)  # Start at the middle

    # State map (e.g., q0=0, q1=1, ..., qH=255)
    all_states = set()
    for t in transitions:
        all_states.add(t['current_state'])
        all_states.add(t['next_state'])
    state_map = {s: i for i, s in enumerate(sorted(all_states))}
    state_map['qH'] = 255  # Halt state

    state = builder.alloca(int8, name="state")
    builder.store(ir.Constant(int8, state_map['q0']), state)

    # Direction mapping
    dir_map = {'L': -1, 'R': 1, 'S': 0}

    # Placeholder logic to avoid empty block error
    # Actual transition logic to be extended for full simulator
    builder.ret_void()
    return module

if __name__ == "__main__":
    mod = codegen_turing_machine(transitions)

    os.makedirs("output", exist_ok=True)
    with open("output/tm.ll", "w") as f:
        f.write(str(mod))

    print("[+] LLVM IR emitted to output/tm.ll")
