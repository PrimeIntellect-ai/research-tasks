You are a Machine Learning Engineer preparing synthetic DNA training data for a sequence motif recognizer. You need to sample a realistic distribution of 10-base DNA primers that align well to a specific reference template but also maintain an optimal GC-content.

Your task is to write a C program that performs Markov Chain Monte Carlo (MCMC) sampling of primer sequences, computes an empirical distribution metric, and logs the results.

Create a C program at `/home/user/generate_primers.c`. The program must do the following:

**1. Scoring System**
The state space consists of all possible 10-character DNA strings (using 'A', 'C', 'G', 'T').
The reference sequence is: `ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAG`
For any 10-mer primer $p$:
*   **Alignment Score $A(p)$:** The maximum number of matching characters when sliding the 10-mer across the reference sequence without any gaps. (e.g., if the 10-mer perfectly matches a substring of the reference, the score is 10. Minimum score is 0).
*   **GC-Content Score $G(p)$:** Let $g$ be the total number of 'G' and 'C' characters in $p$. $G(p) = -1.0 \times (g - 5)^2$.
*   **Total Score $S(p)$:** $A(p) + G(p)$.

**2. MCMC Sampling (Metropolis Algorithm)**
Implement an MCMC sampler to draw sequences proportional to $P(p) \propto \exp(S(p))$.
To ensure exact reproducibility across systems, you **must** use the following custom PRNG:
```c
#include <stdint.h>
uint32_t state = 42;
uint32_t next_rand() {
    state = (state * 1103515245 + 12345) & 0x7FFFFFFF;
    return state;
}
```

*   **Initialization:** Start with the primer `AAAAAAAAAA` as your current state $p$.
*   **Iterations:** Run for exactly $N = 500,000$ steps.
*   **Proposal:** In each step, propose a new sequence $p'$ by mutating the current sequence $p$:
    1.  Pick a random index $i$ in the primer: `int i = next_rand() % 10;`
    2.  Pick a random nucleotide $c$ from the array `char bases[] = "ACGT";` (in that exact order): `char c = bases[next_rand() % 4];`
    3.  Create $p'$ by replacing the character at index $i$ in $p$ with $c$.
*   **Acceptance:** Calculate the acceptance probability $\alpha = \exp(S(p') - S(p))$.
    *   Generate a uniform random float $u$: `double u = (next_rand() % 1000000) / 1000000.0;`
    *   If $u < \alpha$, accept the proposal (set $p = p'$). Otherwise, reject (keep $p$).
*   **Tracking:** Record the GC-count ($g \in \{0..10\}$) of the sequence state at *every* step of the 500,000 iterations (including the start state, and whether a mutation was accepted or rejected).

**3. Probability Distribution Metric**
Calculate the Total Variation Distance (TVD) between the empirical distribution of GC-counts from your 500,000 MCMC samples, and an ideal Binomial distribution $B(n=10, p=0.5)$.
*   $P_{emp}(k) = \text{count of samples with GC-count } k / 500000.0$
*   $P_{ideal}(k) = \binom{10}{k} / 1024.0$
*   $\text{TVD} = 0.5 \times \sum_{k=0}^{10} |P_{emp}(k) - P_{ideal}(k)|$

**4. Output**
Compile your program and run it. The program should write the output to `/home/user/mcmc_results.txt`. The file must contain exactly one line with the calculated TVD formatted to six decimal places.

Example output format for `/home/user/mcmc_results.txt`:
```
0.123456
```