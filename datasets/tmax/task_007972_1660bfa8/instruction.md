You are an AI assistant helping a computational physics researcher analyze stochastic simulation outputs. 

The researcher has generated a large dataset of simulated particle energies, stored in an HDF5 file at `/home/user/sim_data.h5` under the dataset name `energies`. They want to understand how quickly their empirical mode (peak of the energy distribution) converges as the number of simulation samples $N$ increases.

Your task is to write and execute a Python script that performs the following steps:
1. Load the 1D array of floats from the `energies` dataset in `/home/user/sim_data.h5`.
2. For each sample size $N$ in the list `[100, 500, 1000, 2000, 5000, 10000]`, take the *first* $N$ elements of the dataset.
3. For each subset, perform Kernel Density Estimation (KDE) using `scipy.stats.gaussian_kde` with its default bandwidth estimator (Scott's Rule).
4. Find the empirical mode (the energy value that maximizes the KDE PDF) for each subset by evaluating the KDE over a fixed grid of 2000 linearly spaced points between 0.0 and 15.0 (inclusive).
5. Assume the mode calculated using all $N=10000$ samples is the "true" mode $M_{true}$. 
6. Calculate the absolute error $E_N = |M_N - M_{true}|$ for the remaining $N$ values (`100, 500, 1000, 2000, 5000`).
7. Perform a linear least-squares regression (e.g., using `scipy.stats.linregress` or `numpy.polyfit`) on $\log_{10}(N)$ versus $\log_{10}(E_N)$ to find the convergence rate (the slope of the line).
8. Save ONLY the calculated slope, rounded to exactly 4 decimal places, to a text file at `/home/user/convergence_rate.txt`.

Ensure your script handles the required scientific data format and correctly implements the convergence testing through density estimation and regression. You may install any standard scientific python packages (like `h5py`, `numpy`, `scipy`) if they are not already present.