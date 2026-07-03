I am running a simulation that calculates an energy reduction sum, but I suspect we are losing precision due to the floating-point reduction order in our C implementation. 

I need you to perform a regression test and validation using Python.

Here is what you need to do:
1. We need to find a specific simulation parameter `r`. It is the root of the nonlinear equation $f(x) = x^3 - 4x + 1$ within the interval $[0, 1]$. Use Python to solve this equation and find `r` (use double precision / `float64`).
2. There is a C program located at `/home/user/sum_sim.c` which takes this root `r` as a command-line argument. It computes a sum $\sum_{n=1}^{10^6} \frac{r}{n^2 + r^2}$ using single-precision `float` in two different loop orders: forward ($n=1$ to $10^6$) and backward ($n=10^6$ down to $1$).
3. Compile the C program and run it with the root `r` as the argument to get the `forward` and `backward` sum results.
4. To validate these results, write a Python script to compute the exact same sum in double precision (`float64`). This will serve as our analytical ground truth.
5. Compare the C results to the Python ground truth to determine which C reduction order ("forward" or "backward") is more accurate.
6. Create a JSON report at `/home/user/regression_report.json` with exactly the following keys:
   - `"root"`: The root `r` you found (float).
   - `"c_forward"`: The forward sum from the C program (float).
   - `"c_backward"`: The backward sum from the C program (float).
   - `"python_true"`: The high-precision sum calculated in Python (float).
   - `"more_accurate_method"`: A string, either `"forward"` or `"backward"`, indicating which C method was closer to the Python truth.

Ensure the JSON file is valid and contains these precise keys.