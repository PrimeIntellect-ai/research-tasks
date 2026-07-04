You are an assistant helping a researcher optimize, sample, and test a decay model. 

The researcher has a dataset of radioactive decay measurements in `/home/user/data/decay_data.csv` with two columns: `t` (time) and `y` (measured activity).

You need to create an end-to-end Python scientific workflow that performs Optimization, MCMC Sampling, Density Estimation, Visualization, and Regression Testing.

Please do the following:

1. **Install Dependencies**: Ensure `numpy`, `scipy`, `emcee`, `matplotlib`, and `pytest` are installed.
2. **Write the Analysis Script** (`/home/user/sim/run_analysis.py`):
   - Load the data from `/home/user/data/decay_data.csv`.
   - The model is $y(t) = A \exp(-\lambda t) + B$.
   - The Log-Likelihood function assumes Gaussian noise with a fixed standard deviation of $\sigma = 0.5$: $\ln L = -\frac{1}{2} \sum \left( \frac{y_i - (A \exp(-\lambda t_i) + B)}{0.5} \right)^2$.
   - Assume uniform uninformative priors: $A \in [0, 10]$, $\lambda \in [0, 5]$, $B \in [0, 5]$. Return $-\infty$ log-prior outside these bounds.
   - **Optimization**: Use `scipy.optimize.minimize` (Nelder-Mead) on the negative log-posterior to find the Maximum A Posteriori (MAP) estimate. Use an initial guess of $A=4.0, \lambda=0.1, B=0.1$.
   - **MCMC**: Initialize an `emcee` ensemble sampler with 10 walkers. Set the initial state of the walkers in a tiny Gaussian ball (std=1e-4) around the MAP estimate. Run the sampler for 500 steps. Use a fixed random seed `np.random.seed(42)` before setting up the walkers.
   - **Density Estimation**: Discard the first 100 steps (burn-in). Flatten the remaining chain for the parameter $A$. Fit a `scipy.stats.gaussian_kde` to the flattened samples of $A$. Evaluate the KDE on a grid from $A=0$ to $A=10$ (1000 points) to find the "KDE Peak" (the $A$ value where the KDE is maximized).
   - **Visualization**: Create a histogram of the $A$ samples overlaid with the KDE curve, and save it to `/home/user/sim/posterior_A.png`.
   - **Output**: Save the MAP parameters and the KDE peak for $A$ to `/home/user/sim/results.json` with the exact keys: `"A_map"`, `"lambda_map"`, `"B_map"`, and `"A_kde_peak"`. All values should be standard floats.
3. **Write a Regression Test** (`/home/user/sim/test_model.py`):
   - Write a `pytest` test that runs the optimization portion of your analysis and asserts that `A_map` is between 4.9 and 5.1.
4. **Run the Test**: Execute the test using `pytest` and save the standard output to `/home/user/sim/test_results.log`.

Make sure to create the `/home/user/sim/` directory. The dataset will be pre-created for you.