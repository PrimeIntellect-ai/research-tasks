You are tasked with helping a researcher fix a numerical integration issue in an MCMC simulation. 

The researcher is trying to estimate the damping coefficient `gamma` of a damped harmonic oscillator using a Metropolis-Hastings MCMC algorithm. The code is written in C++ and uses an adaptive step-size integrator. However, the MCMC posterior distribution is coming out completely wrong. The researcher suspects that the numerical integrator is diverging or failing because of a bug in how the step-size adaptation is handled when stepping to the exact observation times.

Here is the situation:
1. The project directory `/home/user/mcmc_project` contains `mcmc.cpp`.
2. The script reads observation data from an HDF5 file `observations.h5` (containing 1D float arrays `t` and `y`).
3. The MCMC algorithm tries different values of `gamma`, integrates the trajectory, and compares it to the observations. 
4. The integration function `integrate_to` is supposed to advance the simulation state `(t, y, v)` up to `t_end`. However, the adaptive step size `dt` is not correctly capped, causing the integrator to overshoot `t_end`. This evaluates the simulated trajectory at the wrong times, ruining the likelihood computation.

Your tasks:
1. Fix the bug in `mcmc.cpp` so that the integrator never overshoots `t_end` (i.e., if `t + dt > t_end`, limit `dt` for that step so it hits `t_end` exactly).
2. Compile the C++ program: `g++ mcmc.cpp -lhdf5_cpp -lhdf5 -o mcmc_sim` (ensure any required libraries are linked).
3. Run the compiled `./mcmc_sim`. It will output a file `posterior.txt` containing the sampled values of `gamma`.
4. The researcher has provided a ground-truth posterior distribution in `/home/user/mcmc_project/reference_posterior.h5` (dataset name `samples`). Write a Python script to compute the 1D Wasserstein distance between the samples in `posterior.txt` and the reference samples. You may use `scipy.stats.wasserstein_distance` and `h5py`.
5. Save the computed Wasserstein distance, rounded to 4 decimal places, to a file named `/home/user/mcmc_project/wasserstein_distance.txt`.

Ensure all tasks are done inside the `/home/user/mcmc_project` directory.