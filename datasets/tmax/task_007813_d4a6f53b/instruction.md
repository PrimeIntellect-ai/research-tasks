You are a performance engineer profiling and debugging a Monte Carlo ODE simulation written in C++. 

The simulation code located at `/home/user/mc_ode_sim.cpp` evaluates the final state of multiple Monte Carlo paths for a simple stochastic differential equation. It reads initial conditions from an HDF5 file `/home/user/init_cond.h5`. 

Currently, the code uses a parallel `omp parallel for` loop to compute the paths and aggregates the sum of the final path values using a shared accumulator with a critical section or atomic add. Because floating-point addition is not strictly associative and the thread completion order varies, the simulation produces slightly different results on every run.

Your tasks:
1. **Fix the Reproducibility Issue**: Modify `/home/user/mc_ode_sim.cpp` so that the final sum of the simulated paths is strictly deterministic and perfectly reproducible across multiple runs, regardless of thread scheduling. To achieve this, store the final value of each path in a `std::vector<double>` of size N, and then perform a sequential sum over the vector *after* the parallel region.
2. **Add Bootstrap Confidence Intervals**: Add logic to the C++ code to compute the 95% bootstrap confidence interval of the *mean* of the final path values. Use 10,000 bootstrap resamples. Use `std::mt19937` with a fixed seed of `42` for the resampling process.
3. **Dependencies**: You may need to install `libhdf5-dev` and configure your compilation properly (using `-fopenmp` and `-lhdf5_cpp -lhdf5`).
4. **Execution and Output**: Compile your fixed code to `/home/user/sim.out` and run it. Have the program output exactly three lines to a file named `/home/user/results.txt`:
   - Line 1: The perfectly reproducible sum of all final path values (formatted with `std::fixed` and 6 decimal places).
   - Line 2: The lower bound of the 95% bootstrap CI of the mean (6 decimal places).
   - Line 3: The upper bound of the 95% bootstrap CI of the mean (6 decimal places).

Ensure your resulting executable runs correctly and that `/home/user/results.txt` is created with the specified format.