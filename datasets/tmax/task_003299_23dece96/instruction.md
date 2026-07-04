You are acting as a bioinformatics software engineer. We have a mathematical model that simulates the evolutionary dynamics of nucleotide frequencies over time using an implicit Ordinary Differential Equation (ODE) solver. The heavy lifting is done in a C shared library, which is orchestrated by a Jupyter notebook.

However, we are experiencing two critical issues:
1. The simulation produces non-reproducible total sequence mass results across identical runs. This is caused by a thread-scheduling-dependent floating-point reduction order in the OpenMP parallel section of the C code.
2. The core ODE solver relies on solving a linear system at each implicit step, but the Matrix LU decomposition routine (`solve_lu`) is currently unwritten, returning empty results.

Your task is to fix and execute this workflow:
1. Examine `/home/user/bio_sim.c`. 
2. Fix the `compute_total_mass` function. It currently uses `#pragma omp atomic` for accumulating floating-point values, which causes non-deterministic rounding errors. Modify the OpenMP pragma to perform a deterministic parallel reduction so the results are exactly reproducible down to the bit.
3. Implement the `solve_lu` function in `/home/user/bio_sim.c`. It must solve the linear system $Ax = b$ using LU decomposition. The matrix $A$ is an $n \times n$ diagonally dominant matrix (row-major order). You can perform the factorization in-place on $A$ and store the solution vector in $b$. 
4. Recompile the shared library by running `make` in `/home/user/`.
5. Orchestrate the workflow by executing the Jupyter notebook `/home/user/workflow.ipynb`. You must run it programmatically from the terminal (e.g., using `jupyter nbconvert --to notebook --execute /home/user/workflow.ipynb`). 

The notebook will run the simulation 50 times to assert exact floating-point reproducibility. If successful, it will output the final state of the simulation to `/home/user/sim_result.json`.

Ensure the final JSON file exists and contains the correct solved ODE states.