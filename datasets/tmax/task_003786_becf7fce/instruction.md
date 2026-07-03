You are a performance engineer tasked with profiling and tuning a thermal simulation tool. 

We have a simulation source file located at `/home/user/thermal_sim.c`. This program calculates the cumulative thermal load of an engine over time $x$ using numerical integration. 

Your task is to find the exact time $x$ at which the thermal load reaches exactly `0.25`. Since the source code cannot be modified and is computationally expensive, you must implement a Newton-Raphson root-finding algorithm in Bash to solve this non-linear equation, utilizing numerical differentiation.

Perform the following steps:
1. Compile the C program from source to `/home/user/thermal_sim`. You must link the math library (`-lm`) and use the `-O3` optimization flag.
2. Write a Bash script `/home/user/solve_time.sh` that implements the Newton-Raphson method to solve $F(x) = 0$, where $F(x) = \text{thermal\_load}(x) - 0.25$.
    * Start with an initial guess of $x_0 = 1.0$.
    * Use a step size of $h = 0.001$ for the central difference numerical derivative: $F'(x) \approx \frac{F(x+h) - F(x-h)}{2h}$.
    * Perform exactly 5 iterations of the Newton-Raphson update: $x_{n+1} = x_n - \frac{F(x_n)}{F'(x_n)}$.
    * Use `bc` or `awk` for floating-point arithmetic within the Bash script.
3. The script must execute the compiled binary to get the thermal load. The binary takes a single float argument $x$ and prints the numerical result to stdout.
4. Save the final value of $x$ (after 5 iterations) to `/home/user/result.txt`, formatted to exactly 4 decimal places (e.g., `1.0425`).

Ensure your script is executable (`chmod +x /home/user/solve_time.sh`) and runs without errors.