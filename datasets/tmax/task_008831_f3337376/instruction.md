You are a machine learning engineer preparing training data for a neural network surrogate model. The model will predict orbital anomalies, specifically replacing a computationally expensive iterative solver for Kepler's Equation: 
$E - e \sin(E) - M = 0$

Where:
- $E$ is the eccentric anomaly (the target variable we need to solve for)
- $e$ is the eccentricity ($0 \le e < 1$)
- $M$ is the mean anomaly ($0 \le M \le 2\pi$)

You have been provided a Monte Carlo sampled dataset of inputs at `/home/user/inputs.csv` with the header `id,e,M`. 

Your task is to write a C++ program that acts as a robust data generator, combining nonlinear equation solving, analytical validation, and convergence tracking.

1. Create a C++ program at `/home/user/kepler_solver.cpp` and compile it to `/home/user/kepler_solver`.
2. Implement the Newton-Raphson method to solve for $E$. 
   - Use $E_0 = M$ as the initial guess.
   - The tolerance for convergence is $|f(E)| < 10^{-8}$.
   - Set a maximum of 50 iterations.
3. Your C++ executable must support two modes via command-line arguments:

   **Mode A: Analytical Validation**
   Command: `./kepler_solver --test`
   The program must internally solve and validate the following exact analytical boundary conditions. If the solver's result is within $10^{-8}$ of the expected $E$, the test passes.
   - Test 1: $e = 0.0$, $M = 1.5$ $\rightarrow$ Expected $E = 1.5$
   - Test 2: $e = 0.5$, $M = 0.0$ $\rightarrow$ Expected $E = 0.0$
   - Test 3: $e = 0.5$, $M = \pi$ $\rightarrow$ Expected $E = \pi$ (Use `3.141592653589793` for $\pi$)
   If all tests pass, print exactly `Tests passed` to standard output and exit with code 0. If any fail, print an error and exit with code 1.

   **Mode B: Data Generation**
   Command: `./kepler_solver --run /home/user/inputs.csv /home/user/ml_dataset.csv`
   The program must read the inputs, solve for $E$ for each row, and write the results to `/home/user/ml_dataset.csv`.
   The output CSV must have the header `id,e,M,E,iterations` where `iterations` is the number of Newton-Raphson steps taken to converge. 
   Format the output floats/doubles using standard precision, but ensure $E$ is accurate to at least 8 decimal places.

To complete the task, successfully compile your code, run the tests (`--test`), and generate the dataset (`--run`). Leave the final dataset at `/home/user/ml_dataset.csv`.