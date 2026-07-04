You are a performance engineer tasked with optimizing the parameters of a scientific simulation tool. The simulator has two critical continuous parameters, `x` and `y`, which significantly affect its execution time. 

Your goal is to find the optimal configuration that minimizes the simulator's runtime, verify the performance improvement statistically, and generate a report.

Here are your instructions:

1. **Compile the Simulator**:
   You have been provided with the source code for the simulator at `/home/user/simulator.c`. Compile it into an executable named `/home/user/simulator` using `gcc`. Make sure to link the math library.
   The simulator takes two parameters via command-line flags: `-x` and `-y` (e.g., `./simulator -x 1.0 -y 2.0`). It outputs a single line containing its execution time: `Runtime: <value>`.

2. **Parameter Optimization**:
   Write a Python script that uses `scipy.optimize.minimize` with the `Nelder-Mead` simplex algorithm to find the optimal values for `x` and `y` that minimize the parsed runtime from the simulator's output. 
   - Start your optimization at an initial guess of `x = 0.0` and `y = 0.0`.
   - Once the optimization converges, round the optimal `x` and `y` values to exactly 1 decimal place.

3. **Statistical Hypothesis Comparison**:
   To statistically validate your findings, collect execution time samples:
   - Run the simulator 20 times using the baseline parameters (`x = 0.0`, `y = 0.0`).
   - Run the simulator 20 times using your rounded optimal parameters.
   - Perform an independent two-sample t-test (Welch's t-test, assuming unequal variances) using `scipy.stats.ttest_ind` to compare the baseline runtimes against the optimized runtimes. We expect the optimized runtimes to be significantly lower.

4. **Reporting**:
   Create a JSON file at `/home/user/report.json` containing the results. The JSON must have exactly the following keys:
   - `"optimal_x"`: (float) Your optimal `x` parameter, rounded to 1 decimal place.
   - `"optimal_y"`: (float) Your optimal `y` parameter, rounded to 1 decimal place.
   - `"p_value"`: (float) The p-value from your Welch's t-test.
   - `"t_statistic"`: (float) The t-statistic from your Welch's t-test.

Ensure you have installed any necessary Python libraries (like `scipy`) in your environment.