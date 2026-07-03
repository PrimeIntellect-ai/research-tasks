You are acting as a bioinformatics analyst. We need to model the propagation of a signal through a Protein-Protein Interaction (PPI) network using a Monte Carlo random walk. 

We have a directed network file located at `/home/user/ppi_network.tsv` where each line represents an interaction in the format:
`Source_Protein Destination_Protein Interaction_Probability`
(Columns are tab-separated).

Your task is to write a pure Bash/Awk script at `/home/user/simulate_walk.sh` that simulates this signal propagation.

The script must accept exactly two arguments:
1. The starting protein name (e.g., `A`)
2. A random seed (an integer)

**Simulation Rules:**
1. The simulation must run for exactly `1000` steps (transitions).
2. Use standard `awk` to process the simulation so we can control the random number generator using the provided seed (i.e., use `srand(seed)` at the beginning of your awk logic).
3. At each step, if the current protein $u$ has no outgoing edges, the signal remains at $u$ for that step.
4. If $u$ has outgoing edges, iterate through all destination proteins $v$. For each edge $u \to v$ with weight $w$:
   - Generate a random number $r$ using awk's `rand()` (which returns a float in `[0, 1)`). Note: Generate $r$ exactly once per outgoing edge, processing edges in alphabetical order of their destination protein $v$.
   - Calculate the transition score: $S = w \times r$.
5. The signal moves to the destination protein $v$ that has the **strictly highest** score $S$. If there is a tie, pick the protein that comes first alphabetically.
6. Record the location of the signal after each of the 1000 steps. (Do not count the starting position at step 0).

**Visualization / Output:**
After 1000 steps, print an ASCII histogram of the visit counts for ALL proteins that were visited at least once during the 1000 steps.
Output the list sorted alphabetically by protein name, strictly in the following format:
`PROTEIN [count] : ===...`
Where each `=` represents 10 visits (use integer division, e.g., 25 visits = `==`, 9 visits = ``, 10 visits = `=`).

Example output format:
```
A [125] : ============
B [405] : ========================================
C [470] : ===============================================
```

**Constraints:**
- Use only standard bash shell built-ins, `awk`, and GNU coreutils. No Python, Perl, or R.
- Ensure numerical stability by doing all the floating-point score comparisons directly in `awk`.
- The script must be executable (`chmod +x`).