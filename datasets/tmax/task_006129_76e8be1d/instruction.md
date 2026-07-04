You are an assistant helping a physicist analyze radioactive decay event counts. We have a set of event counts collected over 20 identical time intervals. 

Your task is to estimate the underlying decay rate (Poisson parameter $\lambda$) using Markov Chain Monte Carlo (MCMC) and perform a statistical hypothesis comparison against a baseline theory.

1. The data is located at `/home/user/counts.txt`. It contains 20 space-separated integers.
2. Write a C++ program in `/home/user/mcmc.cpp` that performs a Metropolis-Hastings MCMC sampling to estimate $\lambda$.
   - **Prior:** Uniform distribution over $[0, 15]$.
   - **Proposal Distribution:** Uniformly sample a new candidate $\lambda'$ in the range $[\lambda_{current} - 1.0, \lambda_{current} + 1.0]$. If $\lambda'$ is outside $[0, 15]$, automatically reject it.
   - **Acceptance Probability:** Standard Metropolis-Hastings acceptance ratio based on the Poisson likelihood and uniform prior.
   - **Iterations:** 200,000 total steps.
   - **Burn-in:** Discard the first 20,000 steps.
   - **Initial State:** Start at $\lambda = 1.0$.
3. Compile your program from source using `g++ -O3 mcmc.cpp -o mcmc`.
4. Run your program to calculate the **Posterior Mean** of $\lambda$ (the average of the accepted samples after burn-in).
5. Compare two hypotheses:
   - **H0 (Baseline):** The data comes from a Poisson distribution with $\lambda = 3.0$.
   - **H1 (Alternative):** The data comes from a Poisson distribution with $\lambda$ equal to your calculated Posterior Mean.
6. Calculate the exact Log-Likelihood of the entire dataset under H0 and under H1. (Make sure to include the log-factorial terms in your log-likelihood calculation: $LL = \sum (k_i \ln \lambda - \lambda - \ln(k_i!))$).
7. Output your results to a file exactly at `/home/user/analysis.log` with the following three lines (replace `X.XX` with your floating-point results):
```
Posterior Mean: X.XX
LL H0: X.XX
LL H1: X.XX
```