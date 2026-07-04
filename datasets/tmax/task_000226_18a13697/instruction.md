You are a bioinformatics analyst tasked with processing a large dataset of DNA sequences to identify potentially functional AT-rich regions. 

You have been provided with a file containing 500,000 short DNA sequences at `/home/user/sequences.txt` (one 50-bp sequence per line). You need to test the statistical hypothesis that each sequence comes from an AT-rich alternative model rather than a uniform background null model.

**Models:**
*   **Null Model ($M_0$):** Uniform background where $P(A) = 0.25, P(C) = 0.25, P(G) = 0.25, P(T) = 0.25$.
*   **Alternative Model ($M_1$):** AT-rich region where $P(A) = 0.30, P(C) = 0.20, P(G) = 0.20, P(T) = 0.30$.

**Your Tasks:**
1. Write a C++ program at `/home/user/calc_llr.cpp` that processes each sequence and calculates its Log-Likelihood Ratio (LLR).
2. **Numerical Stability:** To avoid arithmetic underflow from multiplying many small probabilities, you must calculate the LLR in log-space using the natural logarithm (`std::log`). The LLR for a sequence $S$ of length $L$ is: 
   $$LLR = \sum_{i=1}^{L} \left( \log(P_{M_1}(S_i)) - \log(P_{M_0}(S_i)) \right)$$
3. **Parallel Computing:** Use OpenMP (`#pragma omp parallel for`) to parallelize the sequence processing loop.
4. **Hypothesis Comparison:** Count the total number of sequences that significantly reject the null hypothesis, defined as having an $LLR > 5.0$.
5. Write the final count (a single integer) to the file `/home/user/significant_count.txt`.

Compile your code with `g++ -O3 -fopenmp /home/user/calc_llr.cpp -o /home/user/calc_llr` and execute it to produce the output file.