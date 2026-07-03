You are a data scientist tasked with fitting a Bayesian model to count data using a custom Metropolis-Hastings Markov Chain Monte Carlo (MCMC) algorithm. To speed up the sampling, you will run multiple chains in parallel using MPI. Finally, you will use Kernel Density Estimation (KDE) to find the Maximum A Posteriori (MAP) estimate from the posterior samples.

Write a Python script at `/home/user/run_mcmc.py` that implements the following specification.

**1. Data & Model:**
* Read the dataset of counts from `/home/user/data.txt` (one integer per line). These are drawn from a Poisson distribution with unknown rate $\lambda$.
* Assume a uniform prior for $\lambda$ where $\lambda > 0$. The log-posterior is proportional to $\log(\lambda) \sum x_i - N \lambda$, where $N$ is the number of observations and $x_i$ are the data points.

**2. Parallel MCMC Setup (MPI):**
* Use `mpi4py` to distribute the workload. Your script will be executed with `mpirun -np 4 python run_mcmc.py`.
* Each MPI rank must run an independent MCMC chain.
* **Crucial:** To ensure reproducibility, each rank must initialize its NumPy random seed using `np.random.seed(rank * 100)`, where `rank` is the MPI rank (0 to 3).

**3. MCMC Algorithm (per rank):**
* Initialize the chain with $\lambda_0 = 5.0$.
* Run exactly 5000 iterations (steps 1 to 5000). For each iteration $i$:
  1. Propose a new state: $\lambda_{prop} = \lambda_{i-1} + \epsilon$, where $\epsilon$ is drawn from a Normal distribution with mean 0 and standard deviation 0.5 (use `np.random.normal(0, 0.5)`).
  2. If $\lambda_{prop} \le 0$, automatically reject the proposal.
  3. Calculate the log acceptance probability: $\log(\alpha) = \text{LogPosterior}(\lambda_{prop}) - \text{LogPosterior}(\lambda_{i-1})$.
  4. Draw a uniform random number $u \in [0, 1)$ using `np.random.uniform()`.
  5. Accept the proposal if $\log(u) < \log(\alpha)$, setting $\lambda_i = \lambda_{prop}$. Otherwise, $\lambda_i = \lambda_{i-1}$.

**4. Aggregation and Density Estimation:**
* Discard the first 1000 samples of each chain as burn-in (keep samples from iteration 1001 to 5000, inclusive. Total 4000 samples per chain).
* Use MPI to gather all 4000 samples from each of the 4 chains to Rank 0. Rank 0 should concatenate them into a single 1D array of 16,000 samples (ordered by rank: Rank 0's samples, then Rank 1's, etc.).
* Rank 0 must then estimate the posterior density using `scipy.stats.gaussian_kde` on the aggregated samples (using default bandwidth).
* Rank 0 must evaluate the KDE over a grid of 1000 linearly spaced points between 0 and 20 (inclusive) using `np.linspace(0, 20, 1000)`.
* Find the $\lambda$ value on this grid that maximizes the estimated density (the MAP estimate).

**5. Output:**
* Rank 0 must save the aggregated 16,000 samples as a NumPy binary file at `/home/user/samples.npy`.
* Rank 0 must write the MAP estimate to `/home/user/map_lambda.txt`, formatted to exactly 2 decimal places (e.g., `7.42`).

Do not include any `mpirun` commands in your code; assume the user will execute your script using `mpirun -np 4 python /home/user/run_mcmc.py`.