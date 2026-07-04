As a data scientist in a bioinformatics lab, I need you to build a C++ tool to analyze the amino acid distributions of a newly synthesized batch of protein sequences. We want to test whether the amino acid composition follows a uniform distribution (our null hypothesis, $H_0$) or is significantly biased ($H_1$).

We have a FASTA file located at `/home/user/sequences.fasta`. 

Please write a C++ program, saved as `/home/user/analyze_dist.cpp`, and compile it to `/home/user/analyze_dist`. Your program must perform the following tasks:

1. **FASTA Parsing**: Parse the `/home/user/sequences.fasta` file. Ignore header lines (which start with `>`). Concatenate or process the sequence lines to count the occurrences of the 20 standard amino acids (A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y). Ignore any other characters or newline characters.

2. **Probability Distribution & Convergence Testing**: We need to observe how the empirical distribution converges as sample size increases. Compute the empirical probability distribution $P$ of the amino acids using only the first $N$ sequences in the file, for $N \in \{100, 500, 1000, 2000\}$. 

3. **Distance Metric**: For each $N$, calculate the Kullback-Leibler (KL) divergence (in nats, i.e., using the natural logarithm `log()`) between the empirical distribution $P$ and a perfectly uniform distribution $Q$ (where $Q(i) = 1/20 = 0.05$ for all 20 amino acids). 
   Formula: $D_{KL}(P || Q) = \sum_{i} P(i) \ln \frac{P(i)}{Q(i)}$. 
   *Note: If a specific amino acid count is 0, treat $P(i) \ln(P(i)/Q(i))$ as 0.*

4. **Output 1 (Convergence Results)**: Write the computed KL divergences to a CSV file at `/home/user/convergence_results.csv`. The file should have a header line `N,KL_Divergence`, followed by the 4 rows corresponding to $N = 100, 500, 1000, 2000$. Format the KL divergence to 6 decimal places.

5. **Statistical Hypothesis Comparison**: Using the final empirical distribution computed from all $N=2000$ sequences, decide between:
   * $H_0$: The sequences are drawn from a uniform distribution.
   * $H_1$: The sequences are not drawn from a uniform distribution.
   Reject $H_0$ in favor of $H_1$ if the final KL divergence is strictly greater than `0.005`. Write ONLY the string `H0` or `H1` to a file at `/home/user/hypothesis.txt` based on your conclusion.

Requirements:
- You may use standard C++ libraries (e.g., `<iostream>`, `<fstream>`, `<vector>`, `<string>`, `<cmath>`, `<iomanip>`, `<map>`).
- Compile the program using `g++ -std=c++17 -o /home/user/analyze_dist /home/user/analyze_dist.cpp`.
- Execute the compiled program to generate the required output files.