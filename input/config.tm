# Turing Machine: Binary Incrementer
# This machine increments a binary number by 1

q0 1 -> q0 1 R
q0 0 -> q0 0 R
q0 _ -> q1 _ L

q1 1 -> q1 0 L
q1 0 -> q2 1 S
q1 _ -> q2 1 S

q2 1 -> q2 1 S     # <--- Added to prevent undefined transition
q2 0 -> q2 0 S     # <--- Optional: handles any leftover 0s (if needed)
q2 _ -> qH _ S     # Halting state
