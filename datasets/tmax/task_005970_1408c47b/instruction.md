You are a data scientist working on a spatial model of DNA-protein binding. You need to write a C program that determines the binding source location from a genome sequence, estimates the expected binding affinity with confidence intervals, and integrates a spatial density model using domain decomposition and mesh refinement.

Please create a C program at `/home/user/model_fit.c` that performs the following steps:

1. **Primer Sequence Alignment**:
   - Read the DNA sequence from `/home/user/genome.txt` (a single line of characters, no fasta headers).
   - Find the 0-based index of the first exact match of the primer sequence `"TTAGGCAT"`.
   - Calculate the normalized source location `X_s = match_index / total_sequence_length`. (Treat `total_sequence_length` as the number of characters in the file, excluding any trailing newlines).

2. **Bootstrap Confidence Intervals**:
   - Read experimental binding affinity data from `/home/user/affinity.csv`. The file contains 50 floating-point numbers, one per line.
   - Calculate the sample mean ($\mu$) of these 50 values.
   - Perform a bootstrap analysis to find the 95% confidence interval for the mean.
   - Requirements for bootstrap: Use exactly 10,000 resamples. Initialize the random number generator strictly with `srand(42)` and use the standard C `rand()` function to select indices (`rand() % 50`). Compute the mean for each resample, sort the 10,000 means, and pick the 2.5th percentile (index 250) and 97.5th percentile (index 9750) to get `[ci_lower, ci_upper]`.

3. **Mesh Refinement and Domain Decomposition**:
   - The spatial binding density across the 1D tissue sample (from $x=0$ to $x=1$) is modeled as: 
     $$D(x) = \mu \cdot \exp(-50 \cdot (x - X_s)^2)$$
   - You must integrate $D(x)$ over the domain $[0, 1]$ using the Trapezoidal rule.
   - **Domain Decomposition**: Split the integral strictly into two subdomains: $D_1 = [0, X_s]$ and $D_2 = [X_s, 1]$.
   - **Mesh Refinement**: For *each* subdomain independently, start the Trapezoidal integration with `N = 10` intervals (i.e., 11 points). Iteratively double the number of intervals (`N = 20, 40, 80...`) until the absolute difference between the current integral estimate and the previous integral estimate is strictly less than `1e-6`.

4. **Output Verification**:
   - Your C program must write the results to `/home/user/results.json` strictly in the following JSON format:
   ```json
   {
     "X_s": 0.000000,
     "mu": 0.000000,
     "ci_lower": 0.000000,
     "ci_upper": 0.000000,
     "integral_D1": 0.000000,
     "integral_D2": 0.000000,
     "bins_D1": 0,
     "bins_D2": 0
   }
   ```
   *(Output floats to 6 decimal places).*

Compile your C program using `gcc -O2 -o /home/user/model_fit /home/user/model_fit.c -lm` and execute it to generate the JSON file. Do not use any external statistical or numerical libraries outside the C standard library.