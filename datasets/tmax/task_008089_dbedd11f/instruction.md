You have recently inherited a C++ codebase for a 2D Heat Equation solver located in `/home/user/heat_solver`. The previous developer left the project in an unfinished and broken state, and you need to get it working.

You have the following objectives:

1. **Recover Missing Configuration**: The simulation relies on a configuration file named `grid_config.txt`. The previous developer accidentally deleted this file before handing over the repository. Fortunately, the project is a Git repository. You must inspect the Git history or filesystem to recover the deleted `grid_config.txt` file and restore it to `/home/user/heat_solver/grid_config.txt`.
2. **Fix the Build Environment**: The provided `Makefile` is misconfigured and currently fails to build the project. You must diagnose the compilation/linking errors and fix the `Makefile` so that running `make` successfully produces an executable named `heat_sim`.
3. **Debug Convergence Failure**: The solver uses a Jacobi iteration method. Currently, if you force it to run, the algorithm fails to converge, always hitting the maximum number of iterations (`max_iter`) without dropping below the error tolerance (`tol`). You must trace the intermediate states of the simulation, identify the algorithmic flaw in `solver.cpp` causing the convergence failure, and fix the C++ code.
4. **Run and Log**: Once fixed, build the project using `make` and run `./heat_sim`. The program will output a final line containing the number of iterations it took to converge (e.g., `Converged in XXX iterations`). 

Write the final number of iterations (just the integer) to a file at `/home/user/result.txt`.

Ensure your fixes in `solver.cpp` correctly implement the Jacobi method without altering the fundamental math formula (just fix the convergence tracking bug). Do not change the grid dimensions or tolerance specified in the recovered configuration.