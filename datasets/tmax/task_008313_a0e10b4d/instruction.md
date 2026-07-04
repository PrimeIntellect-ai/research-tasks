You are acting as a data scientist modeling the spread of a virus using a Susceptible-Infected (SI) model. You have been provided with messy observational data and the C++ source code for a Monte Carlo simulator.

Your objectives are to:
1. **Reshape Observational Data:** 
   Read the raw daily infection data from `/home/user/raw_data.json`. The data is in a flattened, messy JSON format with keys like `"infection_count_day_X"`. Extract the observed number of infections on Day 30.
   
2. **Compile the Simulator:**
   You have the source code for a stochastic SI simulator at `/home/user/sim_src/sim.cpp`. Compile this C++ file into an executable named `sim` located at `/home/user/sim_bin`. It requires standard C++11 (e.g., `g++ -O3 -std=c++11 /home/user/sim_src/sim.cpp -o /home/user/sim_bin`).

3. **Monte Carlo Simulation Wrapper:**
   The `sim` executable takes three arguments: `beta` (infection rate, float), `N` (total population, int), and `seed` (random seed, int). It prints a single integer: the number of infected individuals at Day 30. 
   Write a Python script that takes a given $\beta$ and evaluates the expected Day 30 infections by running the `sim` executable 100 times (using seeds 1 through 100 inclusive) and calculating the mean. The population `N` is always 1000.

4. **Nonlinear Equation Solving:**
   Use a nonlinear root-finding method in Python (e.g., `scipy.optimize.root_scalar` or `scipy.optimize.fsolve`) to find the exact infection rate parameter $\beta$ (between 0.1 and 0.5) that makes the Monte Carlo expected Day 30 infections equal to the observed Day 30 infections extracted in step 1.

5. **Log the Result:**
   Round the discovered $\beta$ to exactly 4 decimal places and write it to a text file at `/home/user/best_beta.txt`. The file should contain nothing but this single float value.