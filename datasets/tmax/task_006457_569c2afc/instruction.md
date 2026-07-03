I am preparing a training dataset for a machine learning surrogate model. The dataset consists of numerical simulations of a decay process, but I suspect that some of the simulations in my dataset diverged or produced garbage data due to incorrect step-size adaptation in the numerical integrator.

I need you to filter the dataset, validate it against the analytical solution, and compute some statistics on the valid data.

Here are the details:
1. The raw data is located at `/home/user/sim_data.h5`. It is an HDF5 file containing 100 groups named `sim_0` to `sim_99`.
2. Each group contains two datasets: `t` (time points) and `y` (state values).
3. The underlying physical system is a simple decay ODE: $dy/dt = -0.5y$ with $y(0) = 1.0$. The analytical solution is therefore $y_{true}(t) = e^{-0.5t}$.
4. I want you to evaluate each simulation by computing the 1-D Wasserstein distance between the empirical distribution of the simulated `y` values and the exact analytical `y` values at the corresponding `t` points. Use `scipy.stats.wasserstein_distance`.
5. A simulation is considered "valid" if the Wasserstein distance is strictly less than 0.05.
6. Extract the final state value (the last element of `y`) from each *valid* simulation. 
7. Using these valid final state values, calculate the 95% bootstrap confidence interval of their mean. Use `scipy.stats.bootstrap` with `n_resamples=1000`, the `BCa` method, and `random_state=42` to ensure reproducibility.
8. Finally, save the results in a JSON file at `/home/user/results.json` with exactly the following format:
```json
{
  "valid_indices": [1, 4, 5, 8],
  "mean_ci_lower": 0.081234,
  "mean_ci_upper": 0.084567
}
```
*Note: `valid_indices` must be a sorted list of integers representing the indices of the valid simulations.*

You will likely need to install necessary Python libraries (like `h5py` and `scipy`) using `pip`. Let me know when the JSON file is ready!