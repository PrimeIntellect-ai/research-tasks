You are acting as a research assistant for a computational physics lab. We need to integrate a 2D scalar field over a unit square domain using a distributed parallel computing approach to handle large mesh sizes. 

Your task is to implement a parallel 2D numerical integrator using `mpi4py` and `numpy`, and then perform a convergence study by refining the mesh.

Here are the specific requirements:

1. **Environment Setup:**
   Install any necessary system and Python packages to support OpenMPI and `mpi4py`. You have `sudo` privileges if needed (passwordless).

2. **The Integrator (`/home/user/parallel_integrate.py`):**
   Write an MPI-parallelized Python script that calculates the 2D integral of the function:
   $$f(x,y) = \sin(\pi x) \sin(\pi y)$$
   over the domain $x \in [0,1]$ and $y \in [0,1]$.
   
   - The script must accept a command-line argument `--N` which specifies the number of grid *intervals* in both the x and y dimensions (i.e., the grid has $(N+1) \times (N+1)$ points).
   - Use a 2D composite Trapezoidal rule for the integration.
   - **Parallelization strategy (Domain Decomposition):** Divide the work across MPI ranks by splitting the $y$-dimension grid points. Each MPI process should compute the 2D trapezoidal integral for its assigned horizontal sub-domain (a slice of rows). Use `comm.reduce` to sum the partial integrals into the final total on Rank 0.
   - The script should print ONLY the final computed integral as a float to standard output (from Rank 0) and cleanly exit.

3. **The Convergence Study (`/home/user/run_study.sh`):**
   Write a bash script that uses `mpirun` to execute your Python script across 4 MPI processes (`-np 4`). 
   - You must run the integration for the following mesh resolutions: $N = 100, 200, 400, 800$.
   - The bash script must collect the outputs and generate a JSON file at `/home/user/convergence_results.json`.
   - The JSON file must strictly follow this format:
     ```json
     {
       "100": 0.123456789,
       "200": 0.123456789,
       "400": 0.123456789,
       "800": 0.123456789
     }
     ```
     (Where the values are the actual computed integrals for those $N$ values).

Please complete the setup, write the code, and execute your bash script so that `/home/user/convergence_results.json` is generated with the correct results.