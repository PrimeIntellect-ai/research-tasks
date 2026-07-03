You are assisting a researcher investigating the numerical stability of a linear system solver on near-singular inputs. When inputs are ill-conditioned, small random perturbations (noise) in the observation vector can lead to wildly different solution vectors. 

The researcher has left the uncompiled C++ simulation code in the directory `/home/user/sim/`.

Your tasks are to:
1. Compile the C++ program `solver.cpp` located in `/home/user/sim/`. Name the resulting executable `solver`. (It requires C++11 or higher).
2. The `solver` executable accepts a single argument: `--seed <N>`. This sets the random seed for the noise generator. Run the simulation for exactly 10,000 iterations, using seeds `N = 1` through `N = 10000`.
3. Each run will print a single floating-point number to standard output: the $L_2$ norm of the resulting solution vector. Collect all 10,000 norms.
4. Calculate the 95% bootstrap confidence interval of the $L_2$ norms using the empirical percentile method (i.e., find the 2.5th percentile and the 97.5th percentile of the collected norms).
5. Save the result in a file named `/home/user/stability_ci.txt`. The file should contain exactly one line with the lower bound and upper bound separated by a comma, formatted to exactly two decimal places (e.g., `1.23,45.67`).

Be sure to use efficient shell scripting or a short script (Python, etc.) to run the executable and process the outputs.