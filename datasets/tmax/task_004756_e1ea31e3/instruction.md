You are a bioinformatics analyst optimizing a Monte Carlo simulation pipeline for sequence mutation energies. 

We have a C++ program located at `/home/user/mc_sim.cpp` that calculates the cumulative energy of random sequence mutations. Because it simulates millions of variations, it uses OpenMP to parallelize the calculations. However, we have a critical non-reproducibility bug: running the program multiple times with the exact same arguments yields slightly different floating-point results. This is due to the non-deterministic order of floating-point additions across parallel threads (`#pragma omp atomic`).

Your objectives are:

1. **Fix the Non-Determinism in C++**: Modify `/home/user/mc_sim.cpp` so that the total energy calculation is perfectly deterministic across runs for a given number of samples and seed. 
   * *Constraint:* You must keep the parallelization (`#pragma omp parallel for`) for computing the individual energy values, as the energy function is computationally expensive in the real pipeline. 
   * *Hint:* To avoid floating-point reduction order issues, allocate an array to store individual results in parallel, and then sum the array sequentially.

2. **Develop a Python Convergence Tester**: Write a Python script at `/home/user/run_convergence.py` that acts as a convergence testing pipeline. The script must:
   * Compile the fixed C++ program. Use `g++ -O3 -fopenmp /home/user/mc_sim.cpp -o /home/user/mc_sim`.
   * Run the compiled executable for four different sample sizes ($N$): `1000`, `10000`, `50000`, and `100000`. Use the seed `12345` for all runs.
   * Capture the total energy output from standard output for each run.
   * Write the results into an HDF5 file at `/home/user/convergence_results.h5`.

3. **Format the HDF5 Output**: The HDF5 file `/home/user/convergence_results.h5` must contain exactly two datasets at the root level:
   * `N_values`: A 1D dataset containing the sample sizes as 32-bit integers (`[1000, 10000, 50000, 100000]`).
   * `energies`: A 1D dataset containing the parsed total energies as 64-bit floats (`float64`) corresponding to each $N$.

You have `sudo` access if you need to install any packages (e.g., `libhdf5-dev`, `python3-h5py`). 

Here is the initial buggy code for `/home/user/mc_sim.cpp`:

```cpp
#include <iostream>
#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <omp.h>

// Simulates computationally expensive energy evaluation
double compute_energy(int i, int seed) {
    double x = (i * 137.0 + seed) * 0.01;
    return std::sin(x) * std::cos(x * 2.5);
}

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <N> <seed>" << std::endl;
        return 1;
    }
    
    int N = std::atoi(argv[1]);
    int seed = std::atoi(argv[2]);
    
    double total_energy = 0.0;
    
    #pragma omp parallel for
    for(int i = 0; i < N; i++) {
        double e = compute_energy(i, seed);
        // Bug: Non-deterministic floating point addition order
        #pragma omp atomic
        total_energy += e;
    }
    
    std::cout << std::setprecision(15) << total_energy << std::endl;
    return 0;
}
```