You are an assistant helping a computational researcher build a reproducible pipeline in C to estimate the integral of a noisy function using domain decomposition and mesh refinement, and then calculate confidence intervals using the bootstrap method.

Your task is to implement this pipeline entirely in the `/home/user/` directory.

### 1. The Numerical Integration Simulation (`integral.c`)
Write a C program `integral.c` that compiles to an executable named `integral`. It should accept three integer arguments: `Nc` (coarse intervals), `Nf` (fine intervals), and `seed` (random seed).
```bash
./integral <Nc> <Nf> <seed>
```

**Domain Decomposition & Mesh Refinement:**
We are integrating $f(x)$ over the domain $[0, 1]$. The domain is decomposed into three regions:
- Region 1 (Left): $[0.0, 0.4]$, integrated using a coarse mesh of `Nc` equal subintervals.
- Region 2 (Center): $[0.4, 0.6]$, integrated using a fine mesh of `Nf` equal subintervals.
- Region 3 (Right): $[0.6, 1.0]$, integrated using a coarse mesh of `Nc` equal subintervals.

Construct an array of $x$ coordinates strictly in this order: from $0.0$ to $1.0$. The total number of points will be $2 \times Nc + Nf + 1$.
At each point $x_i$, the observed value is $y_i = \exp(-100(x_i - 0.5)^2) + \text{noise}_i$.

**Random Noise Generation:**
To ensure cross-platform reproducibility, do NOT use `rand()`. Implement this specific Linear Congruential Generator (LCG):
```c
unsigned long lcg_state = seed;
double next_rand() {
    lcg_state = (lcg_state * 1103515245 + 12345) % 2147483648;
    return (double)lcg_state / 2147483648.0;
}
```
For every point $x_i$ (from $i=0$ to $i=2Nc+Nf$), compute the noise as `(next_rand() * 0.1) - 0.05`. Ensure you call `next_rand()` exactly once per grid point, in order from left to right.

**Integration:**
Compute the integral using the Trapezoidal Rule over the non-uniform grid $x_i$, $y_i$. Print ONLY the final integral value to stdout as a floating-point number (e.g., using `%f`).

### 2. The Reproducible Pipeline and Bootstrap CI (`pipeline.sh` and `bootstrap.c`)
Write a bash script `pipeline.sh` that automates the workflow:
1. Compiles `integral.c` to `integral`.
2. Runs `integral 10 50 <seed>` for 50 independent runs, where `<seed>` goes from 1 to 50 inclusive.
3. Saves the 50 integral results.
4. Uses a second C program, `bootstrap.c` (which `pipeline.sh` should compile to `bootstrap`), to compute the 95% bootstrap confidence interval for the *mean* of the integrals.

**Bootstrap Procedure (`bootstrap.c`):**
- Read the 50 results.
- Set the seed for your custom LCG: `lcg_state = 42;` (Use the exact same `next_rand` function as above).
- Perform $B = 1000$ bootstrap resamples. For each resample:
  - Draw 50 samples with replacement from the original 50 results. To pick an index (0 to 49), use: `int idx = (int)(next_rand() * 50);` (Call this 50 times per resample).
  - Calculate the mean of these 50 sampled values.
- Sort the 1000 resampled means in ascending order.
- The 95% confidence interval bounds are the 2.5th percentile and 97.5th percentile. Using 0-based indexing, these correspond to the 24th index and 974th index of the sorted array.
- The `bootstrap` program should output the confidence interval to a file exactly at `/home/user/bootstrap_ci.txt` in this exact format:
  `[lower_bound, upper_bound]` (formatted to 6 decimal places, e.g., `[0.123456, 0.134567]`).

Ensure `pipeline.sh` completes the entire execution and produces `/home/user/bootstrap_ci.txt`. Do not require user input during execution. Make sure it has execute permissions.