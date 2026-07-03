You are a bioinformatics analyst tasked with estimating the evolutionary time parameter $T$ for a set of DNA sequences based on a continuous-time Markov chain (CTMC) model of nucleotide substitution.

You are given an instantaneous mutation rate matrix $Q_0$ for 4 nucleotides (A, C, G, T) in `/home/user/q_matrix.csv`.
Due to specific environmental pressures, the mutation rate fluctuates over time. The time-dependent rate matrix is given by:
$Q(t) = Q_0 \cdot f(t)$
where $f(t) = e^{-0.1 \cdot t} \cdot \cos^2(t)$.

The cumulative transition matrix over time $T$ is $P(T) = \text{expm}(R(T))$, where $R(T) = \int_0^T Q(t) dt$ and $\text{expm}$ is the matrix exponential. Note that the matrix integral applies element-wise to $Q_0$. 

A summary statistic of the observed sequence differences is $S_{obs} = 1.25$.
The model predicts this statistic as the Frobenius norm of the difference between the transition matrix and the identity matrix:
$S(T) = \| P(T) - I \|_F$

Your goal is to estimate $T$ using a Bayesian approach and then calculate a bootstrap confidence interval for the posterior median.

Write a Python script `/home/user/analyze_evo.py` that does the following:
1. Set the global random seed strictly using `numpy.random.seed(42)` at the very beginning of the script.
2. Read `/home/user/q_matrix.csv`.
3. Implement numerical integration to compute $\int_0^T f(t) dt$. Use `scipy.integrate.quad` for this scalar integral.
4. Implement a Metropolis-Hastings MCMC sampler to find the posterior distribution of $T$:
    - The likelihood of the observation $S_{obs}$ given $T$ follows a Normal distribution $\mathcal{N}(\mu=S(T), \sigma=0.1)$.
    - Use a Uniform(0, 10) prior for $T$. (If $T \notin [0, 10]$, the prior probability is 0).
    - Use a Normal random walk proposal: $T_{proposed} \sim \mathcal{N}(\mu=T_{current}, \sigma=0.5)$.
    - Start the chain at $T_{initial} = 1.0$.
    - Run the chain for exactly 5000 iterations (where iteration 0 is the initial state, and you make 5000 proposal steps).
    - Discard the first 1000 states as burn-in (keeping 4000 samples).
5. From the 4000 post-burn-in MCMC samples of $T$, calculate the 95% Bootstrap Confidence Interval of the **median**:
    - Draw 1000 bootstrap resamples (each of size 4000, drawn with replacement from the MCMC samples).
    - Calculate the median of each of the 1000 resamples.
    - Calculate the 2.5th and 97.5th percentiles of these 1000 medians using `numpy.percentile`.
6. Save the results as a JSON object in `/home/user/results.json` with keys `"ci_lower"` and `"ci_upper"`. Round the values to 3 decimal places.

Ensure you install any necessary dependencies (e.g., `numpy`, `scipy`) via `pip` before running your script.