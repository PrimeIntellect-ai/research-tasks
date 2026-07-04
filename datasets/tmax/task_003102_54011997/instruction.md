You are a bioinformatics analyst modeling the spatial distribution of a specific transcriptomic feature across a 1D linear tissue sample. We have raw sequence read mappings, but we need to infer the true focal point of the expression using an adaptive mesh and Bayesian inference.

Your task is to write a C++ program `/home/user/mcmc_mapper.cpp` that performs domain decomposition (mesh refinement), calculates log-likelihoods in a numerically stable way, and runs an MCMC simulation to find the posterior mean of the transcript's origin.

### Background and Data
You are provided with `/home/user/reads.csv`, which contains two columns: `location` (a float between 0 and 100) and `count` (an integer). 
The tissue domain is defined on the interval `[0.0, 100.0]`.

### Phase 1: Mesh Refinement (Domain Decomposition)
1. Start with an initial coarse 1D mesh of 10 equal bins: `[0, 10), [10, 20), ... [90, 100]`. (The last bin is inclusive of 100).
2. For each read in the CSV, assign its `count` to the bin that contains its `location`.
3. **Refinement Rule:** Any bin that contains a total read count strictly greater than `500` must be split into two equal-sized sub-bins. Distribute the reads from the parent bin into the two new child bins based on their exact `location`.
4. Perform only **one** pass of refinement (do not recursively split).
5. Output the final number of bins to `/home/user/mesh_stats.txt` in exactly this format:
   `Final bins: <integer>`

### Phase 2: Numerically Stable MCMC & Posterior Estimation
We model the transcript's origin location, $\mu$, using a Normal distribution likelihood.
* **Prior:** $\mu \sim \text{Uniform}(0, 100)$
* **Likelihood:** The observed data is the aggregated reads in your refined mesh. Assume all reads in a bin are located exactly at the *midpoint* ($x_i$) of that bin.
  The likelihood of a single read at $x_i$ given $\mu$ is $N(x_i | \mu, \sigma=5.0)$.
* **Numerical Stability:** Because the total number of reads is large, multiplying the probabilities will cause standard floating-point underflow. You MUST compute the log-likelihood:
  $\log L = \sum_{i=1}^{N_{bins}} c_i \left[ -0.5 \ln(2\pi \sigma^2) - \frac{(x_i - \mu)^2}{2\sigma^2} \right]$
  where $c_i$ is the total count of reads in bin $i$, and $x_i$ is the midpoint of bin $i$.

**MCMC Algorithm (Metropolis-Hastings):**
1. Initialize $\mu^{(0)} = 50.0$.
2. For 10,000 iterations (step $t = 1$ to $10000$):
   a. Propose $\mu' \sim N(\mu^{(t-1)}, \text{step\_size}=1.0)$. (Use a standard C++ `<random>` generator with seed `42`).
   b. If $\mu' < 0$ or $\mu' > 100$, reject the proposal ($\mu^{(t)} = \mu^{(t-1)}$).
   c. Otherwise, compute the acceptance ratio $\alpha = \exp(\log L(\mu') - \log L(\mu^{(t-1)}))$.
   d. Draw $u \sim \text{Uniform}(0, 1)$. If $u < \alpha$, accept ($\mu^{(t)} = \mu'$); else reject ($\mu^{(t)} = \mu^{(t-1)}$).

### Phase 3: Compilation and Execution
1. Compile your code using `g++ -O3 -std=c++17 /home/user/mcmc_mapper.cpp -o /home/user/mcmc_mapper`.
2. Run the program.
3. Discard the first 1,000 samples (burn-in). Calculate the mean of the remaining 9,000 samples of $\mu$.
4. Write this posterior mean to `/home/user/posterior_mean.txt` in exactly this format (rounded to 2 decimal places):
   `Mean mu: <value>`

Ensure both output files are created successfully with the correct values.