# semantic/semantic.py

def check_semantics(transitions):
    print("\n=== SEMANTIC ANALYSIS ===")
    errors = []
    seen = set()
    defined_states = set()

    for t in transitions:
        key = (t['current_state'], t['read_symbol'])

        # Check for duplicate transitions
        if key in seen:
            errors.append(f"Duplicate transition found for state '{t['current_state']}' with symbol '{t['read_symbol']}'")
        else:
            seen.add(key)

        # Track all defined states
        defined_states.add(t['current_state'])
        defined_states.add(t['next_state'])

        # Check for valid directions
        if t['direction'] not in ('L', 'R', 'S'):
            errors.append(f"Invalid direction '{t['direction']}' in transition: {t}")

    # Optionally: check if 'qH' exists as halting state
    if 'qH' not in defined_states:
        errors.append("Missing halting state 'qH'")

    if errors:
        print("Semantic Errors Found:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("No semantic errors detected.")
