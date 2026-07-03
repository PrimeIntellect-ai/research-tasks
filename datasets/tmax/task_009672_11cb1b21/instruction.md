You are a performance engineer tasked with optimizing a scientific simulation.

We have a C program at `/home/user/heat_opt.c` that performs parameter estimation. It tries to find the optimal thermal diffusivity (`alpha`) of a material by simulating a 1D heat equation (PDE) on a spatial mesh and using gradient descent (Optimization) to minimize the error against a known target state. The simulation uses the Backward Euler method, which requires solving a linear system at each time step. 

Currently, the program takes too long to run because it uses a highly inefficient, general-purpose dense LU decomposition to solve the linear system at each step. However, because the implicit Euler discretization of the 1D heat equation on a standard mesh only yields a tridiagonal matrix, you can replace this with a much faster specialized matrix decomposition (the Thomas algorithm).

Your tasks:
1. Profile the code using standard Linux profiling tools (e.g., `gprof`) to confirm the name of the bottleneck function. Write the exact name of this most time-consuming function into `/home/user/bottleneck.txt`.
2. Modify `/home/user/heat_opt.c` to replace the inefficient dense matrix solver with an efficient $O(N)$ tridiagonal solver (Thomas algorithm). The function signature of the bottleneck function should remain the same or be adapted, but it must correctly solve the system $A x = b$ where $A$ is the tridiagonal matrix formed by the Backward Euler method.
3. Compile (with `gcc -O3 -lm heat_opt.c -o heat_opt`) and run the optimized code. It will output the optimal `alpha` value.
4. Save the final optimized `alpha` value (exactly as output by the program, e.g., `0.045123`) to `/home/user/solution.txt`.

Ensure your optimizations maintain mathematical correctness. The simulation output must remain the same (within standard floating-point tolerances) but run significantly faster.