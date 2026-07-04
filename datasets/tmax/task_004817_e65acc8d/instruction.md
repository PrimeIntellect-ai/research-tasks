You are an environmental researcher investigating particle diffusion in a simulated 1D domain. You have a C-based stochastic simulation solver that outputs the empirical distribution of particle positions, but you need to evaluate if refining the mesh changes the final spatial distribution of particles significantly. You will measure this difference using the 1st Wasserstein distance and quantify the statistical uncertainty of this distance using bootstrap confidence intervals.

Perform the following steps:

1. **Compile the Simulator:**
   You will find the C source code for the simulator at `/home/user/sim/sim.c`. Compile it into an executable named `/home/user/sim/sim` using `gcc`. You will need to link the math library.

2. **Run Domain Simulations:**
   Run the compiled simulation twice to simulate two mesh resolutions. The simulator takes two arguments: `<seed>` and `<N>` (number of grid points). 
   - Run the coarse simulation with seed `42` and `N=1000`. Save the standard output to `/home/user/coarse.txt`.
   - Run the fine (refined mesh) simulation with seed `42` and `N=2000`. Save the standard output to `/home/user/fine.txt`.

3. **Compute Distance and Confidence Intervals:**
   Write a Python script to analyze the generated data:
   - Load the particle positions from `coarse.txt` and `fine.txt`.
   - Calculate the 1st Wasserstein distance between the two empirical distributions (using `scipy.stats.wasserstein_distance`).
   - To account for sampling noise, compute a 95% bootstrap confidence interval for this Wasserstein distance. 
   - Procedure for bootstrapping: Set `numpy.random.seed(42)` exactly once before the loop. Perform 1000 bootstrap iterations. In each iteration, draw a random sample with replacement from the coarse data (size 1000) and a random sample with replacement from the fine data (size 2000), then calculate the Wasserstein distance between these two bootstrap samples. Calculate the 2.5th and 97.5th percentiles of these 1000 distances to get the lower and upper bounds of the confidence interval.

4. **Save Results:**
   Output your results to a JSON file located at `/home/user/results.json`. The JSON should contain exactly three keys: `"distance"`, `"ci_lower"`, and `"ci_upper"`. The values must be the calculated floats rounded to exactly 4 decimal places.

Ensure the final JSON file is properly formatted.