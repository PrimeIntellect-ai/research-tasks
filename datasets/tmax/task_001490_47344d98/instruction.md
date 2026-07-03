You are a performance engineer tasked with profiling and optimizing a slow scientific computing application.

We have a C++ application located at `/home/user/mcmc_opt.cpp`. This application reads synthetic experimental data from an HDF5 file (`/home/user/input.h5`), performs Metropolis-Hastings MCMC sampling to estimate the parameters `a` and `b` of a linear model ($y_i = a \cdot x_i + b + \text{noise}$), and finally uses Gradient Descent to find the optimal scalar $z$ that minimizes the function $f(z) = (z - a)^2 + (z - b)^2$.

Currently, the application runs very slowly because it was written by a junior scientist who made a severe performance mistake in the MCMC loop. 

Your tasks:
1. Identify and fix the performance bottleneck in `/home/user/mcmc_opt.cpp`. The logical behavior, random seed, and mathematical steps must remain exactly the same. Only fix the structural inefficiency.
2. Compile the optimized code using `g++` (ensure you link the necessary HDF5 libraries: `-lhdf5_cpp -lhdf5`).
3. Run the compiled executable to produce the output.
4. The executable will print the final optimized $z$ value to standard output. Save this exact output to a file at `/home/user/output.txt`.

Requirements:
- Do not change the random seed (`42`), the number of MCMC steps (`10000`), or the Gradient Descent parameters.
- The compiled executable should be named `/home/user/mcmc_opt`.
- Ensure your output file `/home/user/output.txt` contains only the final float value of $z$ (e.g., `6.251`).