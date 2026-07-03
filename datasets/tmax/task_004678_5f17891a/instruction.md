You are a performance engineer profiling a scientific application. We have a C program at `/home/user/density_sim.c` that performs a simulated density estimation over a network of molecular nodes. The program is parallelized using OpenMP to speed up the heavy node-weight computations.

However, the application produces slightly different floating-point results on every run. This non-reproducibility is due to the floating-point reduction order—specifically, the use of `#pragma omp atomic` for accumulating the `total_density` variable, which causes the additions to occur in a non-deterministic order. 

Your task:
1. Modify `/home/user/density_sim.c` to fix the non-reproducibility. You must keep the OpenMP parallelization for the `compute_node_weight` loop, but you must ensure the final accumulation of `total_density` is strictly deterministic. To do this, store the individual node weights in an array during the parallel loop, and then perform a sequential sum over the array in strictly ascending index order (from `i = 0` to `N-1`).
2. Compile the fixed program using `gcc -fopenmp -O2 -lm density_sim.c -o density_sim`.
3. Run the program and redirect its output to `/home/user/reproducible_density.txt`.

Ensure your sequential reduction sums the elements exactly in the order `0` to `N-1` to guarantee bitwise exactness with our verification suite.