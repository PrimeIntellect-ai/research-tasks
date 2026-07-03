You are a performance engineer assisting a scientific computing team. They need a Python script to process network diffusion data efficiently.

Write a script at `/home/user/fast_sim.py` that performs the following steps:
1. Reads an adjacency matrix `A` (2D array) and an initial state vector `s` (1D array) from the HDF5 file `/home/user/input.h5`.
2. Computes the graph Laplacian matrix $L = D - A$, where $D$ is the diagonal matrix of node degrees (row sums of $A$).
3. Computes the Singular Value Decomposition (SVD) of $L$.
4. Reconstructs a low-rank approximation of the Laplacian, $L_{approx}$, using ONLY the top 5 largest singular values and their corresponding left/right singular vectors.
5. Simulates diffusion by numerically integrating the ordinary differential equation $dx/dt = -L_{approx} x$ from $t=0$ to $t=1.0$ using the explicit Euler method with a time step of $\Delta t = 0.1$. The initial condition is $x(0) = s$.
6. Saves the final state vector $x(1.0)$ (after 10 steps) to `/home/user/output.h5` as a dataset named `x_final`.

Execute your script so that `/home/user/output.h5` is generated.