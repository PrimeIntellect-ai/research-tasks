You are a data scientist analyzing a physical system modeled by the Van der Pol oscillator, a classic non-linear ODE. 

You have observational data stored in an HDF5 file at `/home/user/observational_data.h5`. This file contains three datasets:
- `time`: An array of 500 time steps from t=0 to t=3000.
- `y1`: The observed position of the oscillator over time.
- `y2`: The observed velocity of the oscillator over time.

You have been provided a base simulation script at `/home/user/simulate.py`. This script contains a function `run_simulation(mu, t_eval)` that attempts to numerically integrate the system using `scipy.integrate.solve_ivp` with the default `RK45` method. 

However, the system parameters being analyzed involve high damping/forcing ratios ($\mu \sim 1000$), making the system highly stiff. The current integrator either hangs forever or diverges wildly due to improper step-size adaptation for stiff equations.

Your task is to:
1. Fix `/home/user/simulate.py` by changing the integration method to an appropriate stiff solver (e.g., `BDF` or `Radau`) so that it computes correctly and efficiently. Use relative tolerance `rtol=1e-6` and absolute tolerance `atol=1e-9` in `solve_ivp`.
2. Write an analysis script (e.g. `/home/user/analyze.py`) that loads the observational data.
3. Use your fixed simulation function to generate model predictions for `y1` at the exact time steps in the data, for the following candidate values of $\mu$: `[950, 990, 1000, 1010, 1050]`.
4. For each candidate $\mu$, compute the reduced chi-squared statistic ($\chi^2_\nu$) comparing the modeled `y1` to the observed `y1`. Assume the variance of the observations is strictly $\sigma^2 = 0.1$. The formula to use is: $\chi^2_\nu = \frac{1}{N - p} \sum_{i=1}^N \frac{(y_{1,obs} - y_{1,model})^2}{\sigma^2}$, where $N$ is the number of data points (500) and $p$ is the number of fitted parameters (here, $p=1$).
5. Save your final results into a new HDF5 file at `/home/user/analysis_results.h5`.

The output file `/home/user/analysis_results.h5` must contain exactly:
- A dataset named `mu_tested` containing the candidate $\mu$ values as an array of floats or ints.
- A dataset named `chi_squared` containing the computed reduced chi-squared values in the same order.
- An attribute on the root group (accessible via `f.attrs['best_mu']`) storing the candidate $\mu$ value that produced the lowest $\chi^2_\nu$ (as an integer).