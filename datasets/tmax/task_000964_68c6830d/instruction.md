You are a Machine Learning Engineer preparing training data for a neural network emulator of a physical system. 

You have been provided with MCMC posterior samples stored in an HDF5 file located at `/home/user/mcmc_samples.h5`. The file contains a single dataset named `trajectories` with shape `(num_chains, num_steps, num_dimensions)`.

Unfortunately, the numerical integrator used during the MCMC sampling had a bug with step-size adaptation, causing some chains to diverge and produce extremely large values. 

Your task is to process this data using any programming language of your choice (e.g., Python, R, Julia) to accomplish the following:
1. Read the `trajectories` dataset from `/home/user/mcmc_samples.h5`.
2. Identify and remove any chains that contain at least one value with an absolute magnitude greater than `1000.0`.
3. Extract the first dimension (index 0) from the remaining valid chains and flatten them into a single 1D array of valid posterior samples.
4. Perform a 1D Kernel Density Estimation (KDE) on these valid samples. You must implement or use a standard Gaussian kernel with a fixed bandwidth of `h = 0.5`. The KDE formula to use is:
   `KDE(x) = (1 / (N * h)) * sum( (1 / sqrt(2 * pi)) * exp(-0.5 * ((x - X_i) / h)^2) )`
   where `N` is the number of valid samples, and `X_i` are the valid sample values.
5. Evaluate your KDE at exactly 100 evenly spaced points from `-5.0` to `5.0` (inclusive).
6. Save the 100 evaluated density values to a text file at `/home/user/kde_output.txt`, with one value per line, rounded to 6 decimal places.

Ensure that the output file `/home/user/kde_output.txt` is created with exactly 100 lines.