I am a researcher studying the spatial diffusion of a fluorescent marker in a 2D chemical assay. I have an experimental dataset representing a snapshot of the chemical's concentration, but it is corrupted by Gaussian measurement noise.

I need you to estimate the true amplitude and spatial spread of the chemical concentration using Markov Chain Monte Carlo (MCMC) sampling.

The experimental data is a 2D NumPy array of shape (50, 50) saved at `/home/user/assay_data.npy`.
The physical model for the concentration at integer grid coordinates $(x, y)$ is a 2D Gaussian:
$$ C(x, y) = A \cdot \exp\left( -\frac{(x - 25)^2 + (y - 25)^2}{2 \sigma_{s}^2} \right) $$
where $A$ is the amplitude and $\sigma_{s}$ is the spatial spread. Both $x$ and $y$ indices run from 0 to 49.

The observed data $D$ has known, independent Gaussian noise with standard deviation $\sigma_{noise} = 0.5$. 
Therefore, the log-likelihood of the data given the parameters is:
$$ \ln P(D | A, \sigma_{s}) = \sum_{x=0}^{49} \sum_{y=0}^{49} -\frac{(D_{x,y} - C(x,y))^2}{2 \sigma_{noise}^2} $$

Please write and execute a Python script that does the following:
1. Loads the data from `/home/user/assay_data.npy`.
2. Implements a basic Metropolis-Hastings MCMC algorithm from scratch (do not use external libraries like `emcee` or `pymc`, use `numpy` only) to sample the posterior distribution of $A$ and $\sigma_{s}$.
   - Use uniform priors: $A \sim U(0, 10)$ and $\sigma_{s} \sim U(0.1, 10)$. If a proposal falls outside these bounds, its prior probability is 0 (log-prior = $-\infty$).
   - Run the chain for exactly **5000** iterations.
   - Initial state: $A^{(0)} = 1.0$, $\sigma_{s}^{(0)} = 1.0$.
   - Proposal distributions: independent normal distributions centered on the current state with standard deviation 0.1 for both parameters.
   - Use a fixed random seed `np.random.seed(42)` right before starting your MCMC loop to ensure reproducibility.
3. Calculate the mean of the posterior samples for both $A$ and $\sigma_{s}$ using only the **last 2000** iterations of the chain (i.e., iterations 3000 to 4999, inclusive).
4. Save these estimated means to a text file at `/home/user/posterior_means.txt` in the format: `A: <value>, sigma_s: <value>` (rounded to 3 decimal places).
5. Generate a visualization of your MCMC traces (both parameters plotted against iteration number) and save the plot as `/home/user/mcmc_trace.png`.

Your final outputs must be the script, the `posterior_means.txt` file, and the `mcmc_trace.png` file.