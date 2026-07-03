You are an AI assistant helping a data scientist debug a model.

The data scientist is fitting a kinetic model for primer sequence binding. They have written a C++ program `/home/user/sim.cpp` that:
1. Simulates the primer concentration using an ODE (Euler method).
2. Computes the Discrete Fourier Transform (DFT) of the concentration time series to get the spectral energy.
3. Computes the `total_energy` by summing the spectral energies across all frequencies.

The data scientist is complaining that the output is not strictly reproducible: the `total_energy` fluctuates slightly across different runs with the exact same parameters. This is due to a floating-point reduction order issue caused by the use of `#pragma omp atomic` in the parallel loop.

Your tasks:
1. Fix `/home/user/sim.cpp` so that the `total_energy` is computed perfectly deterministically. Specifically, you must keep the parallel OpenMP loop for computing the individual frequency energies, but store them in a standard container (e.g., `std::vector`) and perform the final sum sequentially *after* the parallel loop.
2. Compile the fixed program to `/home/user/sim` using `g++ -O3 -fopenmp /home/user/sim.cpp -o /home/user/sim`.
3. Perform a numerical convergence test. Run the compiled `./sim <dt>` for the following `dt` (time step) values: `0.1`, `0.05`, `0.025`, and `0.0125`.
4. Log the results of your convergence test into `/home/user/convergence.log`. The file should contain one line per `dt` value (in the order specified) in the exact format:
   `dt,final_P,total_energy`
   where `final_P` and `total_energy` are the exact outputs produced by the program. Do not add any headers or extra spaces.