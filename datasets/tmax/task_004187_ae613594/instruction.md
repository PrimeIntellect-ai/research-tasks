You are a bioinformatics analyst working with sequence transition models. We have modeled DNA sequences as paths through a Markov transition graph, where nodes are nucleotides (A, C, G, T) and edges are the transition probabilities. 

To account for uncertainty in our data, we generated 100 bootstrap resamples of the transition matrix. We need to calculate the probability of observing a specific target sequence for each bootstrapped matrix, and then determine the 95% bootstrap confidence interval for this probability.

However, our current C++ script (`/home/user/calc_prob.cpp`) has two major issues:
1. **Numerical Instability:** The target sequence is 500 bases long. The current code calculates the probability by continuously multiplying transition probabilities, which results in a floating-point underflow (evaluating to exactly `0.0`). 
2. **Missing Bootstrap Analysis:** The code currently only evaluates the first matrix and prints a single probability. 

Your task is to fix and extend `/home/user/calc_prob.cpp`:
1. Modify the probability calculation to be numerically stable. You must compute the **natural logarithm** of the path probability (i.e., the sum of log-probabilities of transitions). Assume the probability of the first nucleotide is always 1.0 (log prob 0.0), so only the 499 transitions are scored. Note that some transitions might have a probability of 0.0 (no edge in the graph); if the sequence takes a missing edge, the overall path probability is 0 (log probability should be negative infinity, or a sufficiently handling mechanism).
2. Calculate the log-probability for the target sequence using **all 100** matrices stored in the 3D array (100 matrices x 4 rows x 4 columns). 
3. Calculate the 95% bootstrap confidence interval of these log-probabilities. Use the percentile method: sort the 100 log-probabilities in ascending order. The lower bound should be the 3rd value (index 2) and the upper bound should be the 98th value (index 97).
4. Output the result to `/home/user/result.txt` exactly in the format:
`[lower_bound, upper_bound]`
Rounded to exactly 4 decimal places (e.g., `[-567.8910, -512.3456]`).

The input files `/home/user/matrices.txt` (containing the 100 matrices) and `/home/user/sequence.txt` (containing the DNA sequence) are already provided and correctly parsed by the boilerplate in `calc_prob.cpp`. The nucleotide mapping is A=0, C=1, G=2, T=3.

Modify the C++ code, compile it using `g++ -O3 -std=c++11 /home/user/calc_prob.cpp -o /home/user/calc_prob`, run it, and ensure `/home/user/result.txt` is generated correctly.