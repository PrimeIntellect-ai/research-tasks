You are assisting a researcher who is running numerical simulations of a population dynamics model. 

The researcher has built a Rust application located at `/home/user/sim_project`. The program solves a simple Ordinary Differential Equation (ODE) using the Euler method for 5000 different initial conditions in parallel using the `rayon` crate. 

Currently, the researcher is facing a problem: the simulation produces non-reproducible statistical results. Upon investigation, they realized that the parallel worker threads are pushing their final results into a shared `Mutex<Vec<f64>>`. Because thread completion order is non-deterministic, the order of the results in the vector changes on every run. When these floating-point results are subsequently reduced or analyzed, the non-associativity of floating-point arithmetic causes small variations, and the scrambled data ruins their time-series alignments.

Your objectives are:

1. **Fix the Rust Simulation**: Modify the Rust code in `/home/user/sim_project/src/main.rs` so that it still processes the simulations in parallel, but collects the results in the exact deterministic order of the initial conditions (`0` to `4999`). Do not remove the parallelization (i.e., keep `rayon`).
2. **Compile and Run**: Build the optimized release version of the Rust code and pipe the output (which prints the 5000 final ODE values, one per line) to `/home/user/results.csv`.
3. **Statistical Analysis (Bootstrap)**: Create a Python script at `/home/user/bootstrap.py` that reads `/home/user/results.csv`.
4. **Compute Confidence Interval**: In the Python script, compute a 95% bootstrap confidence interval for the *mean* of these final values.
    - Use exactly $B=1000$ bootstrap samples.
    - Set the random seed using `numpy.random.seed(42)` before performing any sampling.
    - Use `numpy.random.choice` with `replace=True` to draw the bootstrap samples.
    - Calculate the mean of each sample.
    - Calculate the 2.5th and 97.5th percentiles of these 1000 sample means using `numpy.percentile` (default interpolation).
5. **Log the Result**: The Python script must write the final confidence interval to `/home/user/bootstrap_ci.txt` exactly in this format:
   `95% CI: [lower_bound, upper_bound]`
   (Round the bounds to 4 decimal places, e.g., `95% CI: [123.4567, 125.6789]`).

Ensure all scripts are fully executed and `/home/user/bootstrap_ci.txt` contains the correct reproducible output.