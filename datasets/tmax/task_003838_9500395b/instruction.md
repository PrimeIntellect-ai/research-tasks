You are a bioinformatics analyst tasked with determining the mixture of sequence motifs in a large genomic dataset. 

You have been provided with a Python script `/home/user/solve_mixture.py` that attempts to find the mixture weights of three motifs (Motif A, Motif B, and Motif C) by solving a system of linear equations based on their GC-content signatures. However, the script is currently failing with a singular matrix error because Motif B and Motif C have identical GC-content signatures, making the input matrix near-singular/uninvertible.

Here are the known GC-content probabilities:
- Motif A: 0.75
- Motif B: 0.25
- Motif C: 0.25 (identical to B, drop this from your analysis)

The observed overall GC-content fraction in the genomic dataset is exactly `0.40`.

Your tasks are:
1. **Equation Solving & Validation:** Discard Motif C. Analytically solve the 1D linear equation to find the exact weight (proportion) of Motif A, $w_A$, such that the mixture of Motif A and Motif B produces the observed GC-content of 0.40. 
2. **Monte Carlo Simulation in Bash:** Write a Bash script at `/home/user/simulate.sh` that takes $w_A$ as its first command-line argument. The script must perform a Monte Carlo simulation generating 100,000 random bases. For each base:
    - First, randomly choose between Motif A (with probability $w_A$) and Motif B (with probability $1 - w_A$).
    - Then, generate a G/C base with the chosen motif's GC probability (0.75 for A, 0.25 for B), or an A/T base otherwise.
    - Output the final simulated GC-content fraction (e.g., `0.3985`) to standard output. Use `$RANDOM` in Bash or `awk` for the simulation.
3. **Distance Metric:** Calculate the absolute difference between your simulated GC-content and the observed GC-content (0.40).

**Output Requirements:**
Create a file exactly at `/home/user/results.txt` with exactly two lines:
- Line 1: The exact analytical weight $w_A$ you solved for (e.g., `0.5`).
- Line 2: The absolute difference between your Monte Carlo simulated GC-content and the observed `0.40` (e.g., `0.00154`).

Ensure `/home/user/simulate.sh` is executable and works correctly when run as `./simulate.sh <weight>`.