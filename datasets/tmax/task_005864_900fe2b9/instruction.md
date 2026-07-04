You are a performance engineer analyzing a scientific application. You have been given the source code for a simulation workload, but you need to profile its synthetic metric output to determine the expected performance bounds. 

Your task involves compiling the simulation, running it with OpenMP, and writing a custom C tool to perform a bootstrap confidence interval analysis and distribution fitting on the output.

**Step 1: Compile and Run the Workload**
1. A file named `/home/user/workload.c` has been provided to you. It contains an OpenMP parallelized loop that generates synthetic execution metrics.
2. Compile it to an executable named `/home/user/workload` using `gcc` with OpenMP enabled.
3. Run the executable with exactly 4 OpenMP threads. Redirect its standard output to `/home/user/metrics.txt`. The output will be exactly 100 floating-point numbers, one per line.

**Step 2: Write the Analyzer**
Write a new C program at `/home/user/analyze.c` that does the following:
1. Reads the 100 floating-point numbers from `/home/user/metrics.txt` into an array.
2. Performs a bootstrap analysis to find the 95% confidence interval of the mean, using exactly `10000` bootstrap iterations.
3. For each iteration, you must draw exactly 100 samples with replacement from the original array and calculate their mean. 
4. **Crucial:** To ensure perfectly reproducible results across environments, you *must* use the following deterministic pseudo-random number generator to pick your array indices, rather than the standard `rand()`:
   ```c
   unsigned int state = 42;
   unsigned int my_rand() {
       state = state * 1103515245 + 12345;
       return (state / 65536) % 32768;
   }
   ```
   To draw a sample, pick the index using: `int index = my_rand() % 100;`. Draw the 100 indices sequentially for each of the 10000 iterations.
5. Store the 10000 calculated bootstrap means.
6. Sort the 10000 means in ascending order.
7. Determine the 95% Bootstrap Confidence Interval by finding the 2.5th percentile (index `250`) and the 97.5th percentile (index `9750`). Note: Use exactly these 0-based indices for the lower and upper bounds.
8. Fit a normal distribution to the bootstrap means by calculating the overall mean and the standard deviation (population standard deviation, dividing by N=10000) of the 10000 bootstrap means.

**Step 3: Output the Results**
Your program `/home/user/analyze.c` should write its results to a file named `/home/user/stats.log` in exactly the following format (rounding to 4 decimal places):

```
Mean: <overall_mean>
StdDev: <stddev>
CI_Lower: <lower_bound>
CI_Upper: <upper_bound>
```

Compile and run your `analyze.c` program so that `/home/user/stats.log` is generated.