You are an ML Engineer preparing training data for a biological sequence model. Part of the feature engineering process involves simulating the population dynamics of bacterial strains associated with specific DNA sequences.

The previous engineer left a buggy C script, `/home/user/simulator.c`, which uses numerical integration (Euler's method with variable step size) to calculate the final population state at $T=5.0$ given an initial growth rate $r$. The system being simulated is $dy/dt = r \cdot y \cdot (1 - y/10.0)$, with $y(0) = 0.1$. 

Currently, the numerical integrator diverges and produces `inf` or `NaN` because of a wrong step-size adaptation rule. Specifically, the script increases the time step `dt` when the derivative is large:
`dt = 0.01 * (1.0 + fabs(dydt));`

Your tasks:
1. **Fix the Integrator**: Edit `/home/user/simulator.c` so that the step-size adaptation is inversely proportional to the absolute rate of change. Replace the erroneous line with: `dt = 0.01 / (1.0 + fabs(dydt));`. Ensure `dt` is bounded between `0.0001` and `0.01` (if it falls below `0.0001`, clamp it to `0.0001`). Recompile it as `/home/user/simulator`.
2. **Run Simulations**: You are provided with a CSV file `/home/user/params.csv` containing `Sequence_ID, r_value`. Run the compiled `/home/user/simulator` for each `r_value`. The simulator takes one command line argument (`r_value`) and prints the final integrated value $y(5.0)$ to standard output.
3. **Filter and Reshape**: Determine which `Sequence_ID`s have a final integrated value strictly greater than `2.0`. 
4. **Extract Features**: For the sequence IDs that pass the threshold, extract their corresponding DNA sequences from `/home/user/sequences.fasta`. 
5. **Format Final Dataset**: Reshape the extracted sequences into a tab-separated format where each line contains the Sequence ID (without the `>`) and the sequence on a single line (no line breaks in the sequence string). Save this exactly to `/home/user/training_data.tsv`.

Example output format for `training_data.tsv`:
```
seq1    ATGCATGC
seq3    GGCCGGCC
```

All standard bash tools (awk, sed, grep, etc.) and gcc are available.