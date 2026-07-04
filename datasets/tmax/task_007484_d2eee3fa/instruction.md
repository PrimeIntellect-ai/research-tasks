You are a research assistant helping to complete a scientific simulation pipeline. We are simulating the 3D diffusion of independent particles using a Monte Carlo random walk model, and we need to calculate the Mean Squared Displacement (MSD) along with Bootstrap confidence intervals to quantify uncertainty. 

Finally, you will write a regression testing script to demonstrate convergence.

Please complete the following tasks:

1. **Create the Project Directory:**
   Create a directory at `/home/user/diffusion`. All your files should be placed here.

2. **Write the Simulation Code (`/home/user/diffusion/mc_diffusion.cpp`):**
   Write a C++ program that takes three command-line arguments: `<N>` (number of particles), `<T>` (number of time steps), and `<seed>` (integer random seed).
   
   **Simulation Rules:**
   * Initialize a standard Mersenne Twister generator (`std::mt19937`) with the given `<seed>`.
   * Simulate `N` particles. All particles start at `(0, 0, 0)`.
   * For each particle (from `i = 0` to `N-1`), simulate `T` time steps (from `t = 0` to `T-1`).
   * In each time step, the particle moves in the X, Y, and Z directions simultaneously. Use `std::uniform_int_distribution<int>(0, 1)` to generate a move for each axis. Generate the X move, then Y, then Z. A `1` means a step of `+1`, and a `0` means a step of `-1` in that axis.
   * After `T` steps, calculate the Squared Displacement (SD) for the particle: $X^2 + Y^2 + Z^2$. Store these `N` SD values.
   * Calculate the Mean Squared Displacement (MSD) across all `N` particles.

   **Bootstrap Confidence Interval:**
   * After the simulation, compute a 95% confidence interval for the MSD using Bootstrap resampling.
   * Re-seed the RNG (`std::mt19937`) using `<seed> + 1`.
   * Perform `B = 1000` bootstrap iterations.
   * In each iteration, sample `N` values *with replacement* from your stored SD array. Use `std::uniform_int_distribution<int>(0, N-1)` to generate the indices (generate `N` indices per iteration).
   * Calculate the mean of these `N` sampled SD values (the bootstrap mean).
   * After 1000 iterations, sort the 1000 bootstrap means in ascending order.
   * The 95% CI bounds are the 25th value (index 24) and the 975th value (index 974) of the sorted bootstrap means.

   **Output Format:**
   The program must print exactly one line to standard output in this format:
   `MSD: <msd_value>, CI: [<lower_bound>, <upper_bound>]`
   (Print floating point numbers with their default standard formatting).

3. **Write a Regression and Convergence Test (`/home/user/diffusion/test_convergence.sh`):**
   Write a bash script that:
   * Compiles `mc_diffusion.cpp` into an executable named `mc_diffusion` (use `g++ -O3 -std=c++17`).
   * Runs the executable three times with `<T> = 100`, `<seed> = 42`, and varying `<N>` values: `100`, `1000`, and `10000`.
   * Redirects the standard output of these three runs (in order of increasing `N`) to a log file at `/home/user/diffusion/convergence.log`.

Execute your bash script so the executable is built and the log file is generated.