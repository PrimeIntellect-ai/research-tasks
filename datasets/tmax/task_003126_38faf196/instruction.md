You are a bioinformatics analyst working on a numerical model of protein expression dynamics. You have been provided with a C++ simulation script located at `/home/user/optimize_protein.cpp` and a biologically derived signal in `/home/user/signal.txt`.

The C++ program reads the signal, splits it into 4 segments, and uses multi-threading to compute the Discrete Fourier Transform (DFT) power for a specific target frequency in each segment. It sums these powers to get a `total_power`. 

This `total_power` then drives a simple Ordinary Differential Equation (ODE) representing protein concentration:
dy/dt = total_power - k * y

The script uses a gradient descent optimization loop to find the decay constant `k` that causes the final protein concentration (at t=10.0) to exactly match a target value of `150.0`. The loop performs convergence testing, stopping when the change in `k` is less than `1e-6`.

**The Problem:**
The optimization results are not reproducible. Every time you run the script, the gradient descent takes a different number of iterations or converges to slightly different values of `k`. The convergence test often oscillates. This is because the multi-threaded sum of the DFT powers suffers from non-deterministic floating-point reduction order. The `std::mutex` prevents data races, but the order in which the threads add to `total_power` varies, leading to microscopic floating-point differences that throw off the optimization.

**Your Task:**
1. Fix the C++ code in `/home/user/optimize_protein.cpp` so that the multithreaded accumulation is strictly deterministic. The floating-point addition of the segment powers must occur sequentially in order from segment 0 to segment 3 after the threads have computed their local values.
2. Compile your fixed code using: `g++ -O3 -pthread optimize_protein.cpp -o optimize_protein`
3. Run the compiled program.
4. Save the final optimized `k` value output by the deterministic program into `/home/user/result.txt`. The file should contain ONLY the floating-point number, rounded to 6 decimal places (e.g., `1.234567`).

Do not change the mathematical logic, the optimization hyperparameters, or the ODE integration steps. Only change how the multithreaded reduction is collected.