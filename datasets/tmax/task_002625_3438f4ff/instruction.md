You are a bioinformatics analyst modeling the continuous-time evolution of sequence motif probabilities on a 2D mesh. 

You have been given a C program, `/home/user/simulate_markov.c`, which reads an initial 2D probability distribution from an HDF5 file, performs a time integration of a diffusion-like Markov process (modeling probability mass spreading across sequence states), and writes the final distribution to another HDF5 file.

However, the numerical integrator diverges. The program produces negative probabilities and NaNs because the step-size adaptation (or in this case, the fixed time step `dt`) violates the Courant–Friedrichs–Lewy (CFL) stability condition for the 2D explicit Euler method used in the code.

Your tasks:
1. Inspect `/home/user/simulate_markov.c`. Identify the stability constraint for the 2D diffusion equation: `dt <= (dx^2 * dy^2) / (2 * D * (dx^2 + dy^2))` (which simplifies to `dt <= dx^2 / (4*D)` if `dx == dy`).
2. Fix the bug in `/home/user/simulate_markov.c` by changing `dt` to the maximum stable value (i.e., exactly `dx^2 / (4*D)`).
3. Recompile the program using `h5cc /home/user/simulate_markov.c -o /home/user/simulate_markov`.
4. Run the simulation: `/home/user/simulate_markov /home/user/init.h5 /home/user/out.h5`. (The program always runs for exactly `T = 10.0` simulation time units).
5. We have provided a reference distribution in `/home/user/ref.h5`. Compute the Total Variation (TV) distance between the probability distribution in `out.h5` and `ref.h5`. Both files contain a single dataset named `P` of size 50x50. The Total Variation distance between two discrete distributions $P$ and $Q$ is defined as $TV(P, Q) = \frac{1}{2} \sum_{i,j} |P_{i,j} - Q_{i,j}|$.
6. Write the calculated Total Variation distance to `/home/user/tv_distance.txt`, rounded to exactly 4 decimal places.

Ensure you install any necessary HDF5 utilities or Python libraries if you wish to use Python for the final calculation. You have full `sudo` privileges to install packages (e.g., `libhdf5-dev`, `python3-h5py`) if they are missing.