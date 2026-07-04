You are a performance engineer trying to optimize a black-box microservice. We have a command-line benchmarking tool located at `/usr/local/bin/run_workload` that simulates a standard load test and outputs the average latency in milliseconds. 

The tool takes a single float configuration parameter, the memory pool scale `p`, using the flag `-p` (e.g., `/usr/local/bin/run_workload -p 10.5`). 

Your goal is to find the optimal parameter `p` that minimizes the latency. Because the exact performance curve is unknown and evaluating it is "expensive" (in a real scenario), you must use **Gradient Descent** with **Numerical Differentiation**.

Write a Bash script at `/home/user/optimizer.sh` that implements this.
Your script must:
1. Start with an initial guess of `p = 0.0`.
2. Use a learning rate of `0.05`.
3. Use a central difference method for numerical differentiation to compute the gradient of the latency with respect to `p`. Use a step size of `h = 0.1` for the derivative calculation: `f'(p) ≈ (f(p + h) - f(p - h)) / (2h)`.
4. Run the gradient descent for exactly `50` iterations.
5. You must write the optimization logic entirely in Bash (you may use standard Linux utilities like `bc` or `awk` for floating-point math).
6. After 50 iterations, save the final optimized value of `p`, rounded to exactly 2 decimal places, into the file `/home/user/optimal_p.txt`.

Ensure your script is executable and run it to produce the final output file.