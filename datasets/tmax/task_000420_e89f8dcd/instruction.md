You are a bioinformatics researcher modeling the melting temperature ($T_m$) of a DNA primer under fluctuating environmental conditions. To test the numerical stability of variance algorithms used in your pipeline, you will perform a Monte Carlo simulation.

A primer sequence is located at `/home/user/primer.fasta`.

Your task:
1. Parse the sequence from `/home/user/primer.fasta` (ignore the fasta header) and calculate its length $L$ and its GC content percentage ($GC\% = \frac{G + C}{L} \times 100$).
2. Simulate 100,000 iterations of environmental conditions. In each iteration, the sodium ion concentration $[Na^+]$ is drawn from a uniform distribution between $0.01$ and $0.1$ Molar. 
   *(Use Python for this. Set `numpy.random.seed(42)` and draw all 100,000 samples at once using `numpy.random.uniform(0.01, 0.1, 100000)`).*
3. For each sample, calculate the melting temperature $T_m$ using the following formula:
   $T_m = 81.5 + 16.6 \times \log_{10}([Na^+]) + 0.41 \times GC\% - \frac{600}{L}$
4. To test numerical stability, add an artificially massive baseline offset of $1,000,000,000$ ($10^9$) to every computed $T_m$ value. Store these shifted values in a standard 64-bit float NumPy array.
5. Compute the variance of these shifted $T_m$ values using two different methods:
   - **Method A (Naive one-pass):** $Var_{naive} = \frac{\sum (x^2) - \frac{(\sum x)^2}{N}}{N}$
   - **Method B (Two-pass):** $Var_{twopass} = \frac{\sum (x - \mu)^2}{N}$ where $\mu = \frac{\sum x}{N}$.
   *(Do not use NumPy's built-in variance function for Method A, implement the naive mathematical formula exactly as written using basic NumPy sums: `np.sum(x**2)` and `np.sum(x)`).*
6. Save the results in a file named `/home/user/variance_results.csv` containing a single line with the two values separated by a comma (rounded to 4 decimal places):
   `Naive_Variance,TwoPass_Variance`

Ensure your script runs and writes the file correctly.