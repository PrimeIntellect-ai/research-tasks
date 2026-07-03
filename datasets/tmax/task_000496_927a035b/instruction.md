I am a computational biology researcher modeling a synthetic gene circuit. I need your help to analyze some sequence and expression data.

There are two parts to this task.

**Part 1: Promoter Sequence Alignment**
I have a genome file located at `/home/user/data/genome.fasta`. I need to find the exact starting position of the synthetic promoter sequence `ATGCGTACGTTAG` within the sequence (ignoring any FASTA header lines and treating the sequence as a single contiguous string). 
Find the 0-based index of the first occurrence of this sequence and save the integer value to `/home/user/promoter_index.txt`.

**Part 2: ODE Parameter Estimation via MCMC**
The synthetic gene's protein expression was measured over time, and the noisy data is stored in `/home/user/data/expression_data.csv` (which has two columns: `time` and `protein`).
The protein concentration $p(t)$ is modeled by the following Ordinary Differential Equation (ODE):
$$ \frac{dp}{dt} = k_{prod} - k_{deg} \cdot p $$
where $p(0) = 0.0$.

I need you to write a Python script to estimate the parameters $k_{prod}$ and $k_{deg}$ using Markov Chain Monte Carlo (MCMC) with the `emcee` library.
Here are the exact specifications for the MCMC:
1. **Model:** Solve the ODE numerically (e.g., using `scipy.integrate.odeint`) or analytically to get the expected $p(t)$ for a given pair of $(k_{prod}, k_{deg})$.
2. **Likelihood:** Assume the measured protein concentration has independent Gaussian noise with a known standard deviation $\sigma = 0.5$.
3. **Prior:** Use Uniform(0, 10) priors for both $k_{prod}$ and $k_{deg}$. If a proposal is outside this range, the log-prior is $-\infty$.
4. **MCMC Configuration:**
   - Use `emcee.EnsembleSampler`.
   - Number of walkers: 32.
   - Number of steps: 2000.
   - Initial state: Set the numpy random seed to `42` (`np.random.seed(42)`). Initialize the 32 walkers in a tight Gaussian ball around the initial guess `[1.0, 1.0]` with a standard deviation of `0.1`.
5. **Analysis:** Discard the first 500 steps of each walker as burn-in. Flatten the remaining samples. Calculate the mean of the posterior samples for $k_{prod}$ and $k_{deg}$.

Finally, round the two estimated means to exactly 1 decimal place and save them as a comma-separated string (format: `k_prod_mean,k_deg_mean`, e.g., `1.2,0.5`) in `/home/user/params.txt`.

You will likely need to install `emcee`, `scipy`, `numpy`, and `pandas` in your Python environment.