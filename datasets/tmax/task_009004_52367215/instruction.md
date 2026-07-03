You are an AI assistant helping a researcher optimize a 2D material's structural parameter $k$ to maximize a specific performance metric, calculated via a surface integral. You must implement a multi-language pipeline (C++ and Python) that combines Monte Carlo integration, domain decomposition (mesh refinement), and random-search optimization to find the best parameter and verify its numerical stability.

### Step 1: C++ Monte Carlo Integrator (`/home/user/mc_integrate.cpp`)
Write a C++ program that estimates the integral of the function:
$g(x,y) = \max(0.0, \sin(k \cdot x) \cdot \cos(k \cdot y))$
over a specific rectangular domain using Monte Carlo sampling.

The program must compile to `/home/user/mc_integrate` and accept exactly 7 command-line arguments (all passed as floating-point or integer strings):
`./mc_integrate <k> <x_min> <x_max> <y_min> <y_max> <samples> <seed>`

**Constraints for C++:**
To ensure cross-platform deterministic results, **do not** use `std::mt19937`. Instead, implement this exact Linear Congruential Generator (LCG) inside your C++ code to generate the random $(x, y)$ coordinates:
```cpp
unsigned int current_seed = seed; // parsed from command line
double my_runif(unsigned int& s, double min_val, double max_val) {
    s = (1103515245 * s + 12345) % 2147483648;
    return min_val + (max_val - min_val) * ((double)s / 2147483648.0);
}
```
For each sample (from `0` to `samples - 1`), generate `x` then `y` using the LCG:
```cpp
double x = my_runif(current_seed, x_min, x_max);
double y = my_runif(current_seed, y_min, y_max);
```
Evaluate $g(x, y)$ for all samples, average the results, and multiply by the area of the domain `(x_max - x_min) * (y_max - y_min)` to get the estimated integral. The program should print **only** the final integral value to standard output as a floating-point number.

Compile your code using: `g++ -O3 mc_integrate.cpp -o mc_integrate`

### Step 2: Python Optimizer and Stability Tester (`/home/user/optimize.py`)
Write a Python script that orchestrates the C++ binary to find the optimal $k$ and tests numerical stability across different mesh resolutions. 

The global integration domain is $[0, \pi] \times [0, \pi]$ (use `math.pi`).
You must test three mesh resolutions: $N = 2, 4, 8$.
For a given $N$, the global domain is uniformly divided into an $N \times N$ grid of sub-domains (domain decomposition).

For each $N \in [2, 4, 8]$ (in that order):
1. Reset the Python random seed at the start of the loop for this $N$: `random.seed(42)`
2. Generate exactly 50 candidate values of $k$ using a list comprehension: `k_vals = [random.uniform(1.0, 5.0) for _ in range(50)]`
3. For each candidate $k$:
   - Calculate the global integral by summing the integrals of all $N \times N$ sub-domains.
   - For each sub-domain, call your `./mc_integrate` binary using `subprocess`.
   - Pass `1000` for the `samples` argument.
   - Pass `42` for the `seed` argument to *every* C++ call (each sub-domain starts with seed 42).
   - Iterate sub-domains by row (i from 0 to N-1), then by column (j from 0 to N-1), where $x_{min} = i \cdot \pi / N$ and $y_{min} = j \cdot \pi / N$.
4. Identify `best_k` (the $k$ value that produced the maximum global integral) and the corresponding `max_integral`.

### Step 3: Output Log
The Python script must save the results to `/home/user/stability_results.csv`.
The CSV must have the following exact header and 3 rows of data (one for each $N$):
```csv
N,best_k,max_integral
2,<best_k_rounded_to_4_decimals>,<max_integral_rounded_to_4_decimals>
4,<best_k_rounded_to_4_decimals>,<max_integral_rounded_to_4_decimals>
8,<best_k_rounded_to_4_decimals>,<max_integral_rounded_to_4_decimals>
```

Run your Python script to generate the final CSV.