You are a data scientist analyzing a set of synthetic DNA sequences. You need to write a C program that parses a FASTA file, uses a Monte Carlo method to estimate a specific sequence-dependent integral, parallelizes the workload with OpenMP, and finally fits a linear regression model to the results.

Here are the specific requirements:
1. Create a C program at `/home/user/analyze.c`.
2. The program must read a FASTA file located at `/home/user/sequences.fasta`. This file contains multiple DNA sequences.
3. For each sequence, calculate the GC-content $p$ (the fraction of 'G' and 'C' characters out of the total sequence length).
4. For each sequence, estimate the integral of the function $f(x) = p \cdot x^2 + (1-p) \cdot x$ from $x = 0$ to $x = 10$ using a Monte Carlo integration method with exactly $N = 100000$ random samples. 
   - To ensure reproducibility in the verification test, DO NOT use a random number generator. Instead, simulate the uniform random samples $x_i$ for $i = 0$ to $N-1$ using the deterministic formula: $x_i = ( (i \cdot 137) \pmod{100000} ) / 10000.0$.
   - Calculate the average of $f(x_i)$ and multiply by the interval width (10) to get the estimated area $A$.
5. The calculation of the areas for the different sequences MUST be parallelized using OpenMP (`#pragma omp parallel for`).
6. After calculating the estimated area $A$ for all sequences, perform a simple linear regression across all sequences to fit the model: $A = m \cdot L + c$, where $L$ is the length of the sequence. Calculate the slope $m$ and intercept $c$ using the standard least-squares formulas.
7. Write the final slope $m$ and intercept $c$ to `/home/user/regression.txt` in the exact format:
`Slope: <m>`
`Intercept: <c>`
(Format to 4 decimal places, e.g., `Slope: 1.2345`).

Compile your program using `gcc -O2 -fopenmp /home/user/analyze.c -o /home/user/analyze` and run it to produce the output file.

For setup, assume `/home/user/sequences.fasta` is already present.