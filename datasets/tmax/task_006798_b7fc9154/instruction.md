You are a machine learning engineer generating synthetic training data representing a chemical decay process. You need to find the decay constant that best matches some empirical target data before generating the full dataset.

The target dataset is located at `/home/user/target.txt`. It contains 10 lines of floating-point numbers, representing the observed quantity $Y$ at times $t = 1.0, 2.0, 3.0, \dots, 10.0$.

Your task is to write a standalone Rust program `/home/user/find_k.rs` (using only the standard library) that does the following:
1. Simulates the ordinary differential equation (ODE) $dy/dt = -k \cdot y$ using the forward Euler method.
2. The simulation must start at $t = 0$ with an initial condition $y(0) = 100.0$.
3. Use a time step of $\Delta t = 0.1$.
4. Extract the simulated values $Y_{gen}(t)$ at exact intervals $t = 1.0, 2.0, \dots, 10.0$ (i.e., every 10 steps).
5. Compute the Mean Squared Error (MSE) between the 10 simulated values and the 10 values read from `/home/user/target.txt`.
6. Perform a grid search optimization over the parameter $k$, testing values from $0.00$ to $1.00$ inclusive, in increments of exactly $0.01$.
7. Find the value of $k$ that minimizes the MSE.
8. The program must print only the optimal $k$ to standard output, formatted to exactly two decimal places (e.g., `0.52`).

After writing the program, compile it using `rustc` and run it. Redirect its output (the optimal $k$) to a file named `/home/user/optimal_k.txt`.

Requirements:
- Do not use `cargo` or external crates; rely entirely on `rustc` and `std`.
- Ensure your Euler method accurately multiplies the step size $\Delta t$ correctly: $y_{n+1} = y_n + (-k \cdot y_n) \cdot \Delta t$.
- The output file `/home/user/optimal_k.txt` must contain only the optimal $k$ value (e.g., `0.42`).