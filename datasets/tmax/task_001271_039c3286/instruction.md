You are a performance engineer working on a bioinformatics application. We have a pipeline that calculates a sequence-specific decay metric based on DNA sequences provided in FASTA format. 

Currently, our pipeline uses a numerical ODE integrator to simulate this decay, but it is producing inaccurate results and sometimes diverging because it uses a naive constant step-size. 

Your tasks:
1. Inspect the image at `/app/specification.png`. It contains the correct mathematical rules for the adaptive step-size ODE integration and the analytical validation formula.
2. In `/home/user/`, you will find a buggy script `decay_simulator.py` that currently reads a single FASTA sequence from standard input (stdin), computes `K` (the GC content ratio: count(G+C) / length), and runs a constant step-size Euler integration.
3. Rewrite `decay_simulator.py` so that it parses the FASTA sequence from standard input, calculates `K`, and implements the exact adaptive step-size logic and analytical validation formula described in the image.
4. Your script must print exactly two space-separated numbers to standard output: the numerical final `x` and the analytical final `x`, both formatted to exactly 4 decimal places (e.g., `45.1234 44.9876`).

Requirements:
- Your solution must be written in Python 3 (`/home/user/decay_simulator.py`).
- The program should read the FASTA data from `sys.stdin`. (Ignore FASTA header lines starting with `>`).
- It must exactly match the output of our reference oracle binary under extensive fuzz testing with random DNA sequences.

Fix the code so that it correctly implements the adaptive numerical integrator and validates it against the analytical solution.