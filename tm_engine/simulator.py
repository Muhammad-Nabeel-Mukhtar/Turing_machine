# tm_engine/simulator.py

def run_turing_machine(transitions, input_tape):
    """
    Simulates the execution of a Turing Machine.

    Parameters:
        transitions (list of dict): The parsed TM transitions.
        input_tape (str): The input binary tape (e.g., '1101').

    Returns:
        str: The final tape after halting.
    """

    tape = list(input_tape) + ['_']
    head = 0
    state = 'q0'
    steps = 0
    max_steps = 1000

    # Uncomment for debugging in local console
    # print("=== Turing Machine Execution ===")

    while steps < max_steps:
        current_symbol = tape[head] if head < len(tape) else '_'
        transition_found = False

        for t in transitions:
            if t['current_state'] == state and t['read_symbol'] == current_symbol:
                # print(f"→ State: {state} Read: {current_symbol} → "
                #       f"Write: {t['write_symbol']} Move: {t['direction']} → {t['next_state']}")

                tape[head] = t['write_symbol']
                direction = t['direction']
                state = t['next_state']

                if direction == 'R':
                    head += 1
                    if head >= len(tape):
                        tape.append('_')
                elif direction == 'L':
                    head = max(0, head - 1)
                # Stay (S) means no change in head

                transition_found = True
                break

        if not transition_found:
            # print(f"✖ No transition for state '{state}' and symbol '{current_symbol}'")
            break

        steps += 1

    # print("\n✅ Final Tape:")
    # print(''.join(tape).rstrip('_'))
    return ''.join(tape).rstrip('_')
