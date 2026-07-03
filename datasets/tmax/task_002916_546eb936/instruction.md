You are a data scientist tasked with fitting a non-linear astrophysical model to a set of observations using Markov Chain Monte Carlo (MCMC). You will need to write a C program that reads data from a FITS file, solves a non-linear equation, performs the MCMC sampling, and writes the resulting posterior chains to an HDF5 file. You will also create a reproducible build and test pipeline.

**Background:**
We are modeling the radial velocity $V$ of a star. The model depends on the "mean anomaly" $M$ (the independent variable), the semi-amplitude $K$, and the orbital eccentricity $e$.
The model is defined by two equations:
1. $E - e \sin(E) = M$ (Kepler's Equation). $E$ is the "eccentric anomaly".
2. $V_{model} = K \cos(E)$

**Your Tasks:**

1. **Write the C Application (`/home/user/workspace/mcmc_fitter.c`):**
   * **Input:** Read a FITS binary table located at `/home/user/data/observations.fits`. The table contains 100 rows and two 64-bit float columns: `M` and `V`. You must use CFITSIO.
   * **Non-linear Solver:** Implement a Newton-Raphson solver to find $E$ given $M$ and $e$. Use an initial guess of $E_0 = M$. The solver should iterate until $|E_{new} - E_{old}| < 10^{-6}$, up to a maximum of 50 iterations.
   * **MCMC Algorithm (Metropolis-Hastings):**
     * **Log-Likelihood:** $\ln \mathcal{L} = -0.5 \sum_{i=1}^{100} (V_i - V_{model,i})^2$ (assuming variance is 1.0).
     * **Priors:** Uniform for both parameters: $K \in [0, 100]$ and $e \in [0, 0.99]$. If a proposal falls outside these bounds, reject it immediately (Log-Likelihood = $-\infty$).
     * **Proposals:** Use Gaussian random walks: $K_{new} \sim \mathcal{N}(K_{old}, \sigma_K^2)$ and $e_{new} \sim \mathcal{N}(e_{old}, \sigma_e^2)$. Use $\sigma_K = 1.0$ and $\sigma_e = 0.05$.
     * **Initialization:** Start the chain at $K = 10.0$ and $e = 0.1$.
     * **Iterations:** Run the chain for exactly 10,000 steps (including the initial state as step 0).
     * **Random Seed:** Initialize your random number generator with `srand(42)`. You can use standard `<stdlib.h>` functions (`rand`) or write your own Box-Muller transform for the Gaussian proposals.
   * **Output:** Write the MCMC chains to an HDF5 file at `/home/user/workspace/chain.h5`. Create two datasets named `/K` and `/e`, each being a 1D array of 10,000 elements of type `H5T_NATIVE_DOUBLE`.

2. **Write a Makefile (`/home/user/workspace/Makefile`):**
   * It should compile `mcmc_fitter.c` into an executable named `mcmc_fitter`.
   * It must correctly link the CFITSIO (`-lcfitsio`), HDF5 (`-lhdf5`), and Math (`-lm`) libraries.
   * Include a `clean` target.

3. **Write a Regression Test (`/home/user/workspace/test.sh`):**
   * Write a bash script that cleans the workspace using the Makefile, builds the application, and runs it.
   * After running, it should use `h5dump` or a Python one-liner to verify that `/home/user/workspace/chain.h5` exists and contains 10,000 elements in the `/K` dataset.
   * The script should exit with code 0 if successful, and non-zero otherwise.

*Note: The required system packages `libcfitsio-dev`, `libhdf5-dev`, and `hdf5-tools` are already installed on the system.*