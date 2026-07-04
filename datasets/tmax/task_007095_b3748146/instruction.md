You are a bioinformatics analyst tasked with simulating the accumulation of mutations in a DNA sequence over time using a Monte Carlo approach, and fitting a theoretical model to the results. You will need to write a parallelised Python script to speed up the simulation.

Please perform the following steps:
1. Create a Python virtual environment at `/home/user/venv` and install `mpi4py`, `numpy`, and `scipy`.
2. Write a Python script at `/home/user/mc_evo.py`.
3. The script must use `mpi4py` to run a Monte Carlo simulation across multiple MPI ranks. 
4. The simulation details:
   - Initial sequence: A DNA sequence consisting of exactly 500 'A's.
   - Total number of independent trajectories (simulations) across all ranks: 4000. (Assume the script will be run with an MPI size that perfectly divides 4000, like 4 ranks). Each rank should handle `4000 // size` trajectories.
   - Time steps: Simulate $T=100$ discrete time steps (from $t=1$ to $t=100$), plus the initial state at $t=0$.
   - Mutation rule: In each time step, *each* base in the sequence has a $p=0.01$ probability of mutating. If it mutates, it changes to one of the *other* 3 bases (C, G, or T) with equal probability (though for Hamming distance, the specific base doesn't matter as long as it's not A). Note that previously mutated bases can mutate again (even back to 'A', which reduces the distance).
   - At each time step $t \in [0, 100]$, compute the Hamming distance between the current mutated sequence and the original all-'A' sequence.
5. After simulating the trajectories, the script must gather the data to Rank 0. Rank 0 should compute the global average Hamming distance across all 4000 trajectories for each of the 101 time points (including $t=0$).
6. Rank 0 must then use `scipy.optimize.curve_fit` to fit the theoretical Jukes-Cantor distance model to the averaged data. The model to fit is:
   $D(t) = 375 \times (1 - e^{-k \cdot t})$
   You need to find the best-fit parameter $k$.
7. Finally, Rank 0 should write the fitted value of $k$ to the file `/home/user/fit_result.txt`, formatted to exactly 4 decimal places (e.g., `0.0133`).

You should run your script to ensure it works and produces the file. You can test it using `mpiexec -n 4 /home/user/venv/bin/python /home/user/mc_evo.py`.