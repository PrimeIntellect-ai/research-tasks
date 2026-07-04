You are acting as a machine learning engineer preparing synthetic spectroscopy training data. We need to verify that our new Monte Carlo photon simulation algorithm produces spectral distributions that statistically match our empirical baseline data.

Your task is to write a C program that simulates photon detection and performs a regression test using a probability distribution distance metric. 

Here are the exact specifications for the program:
1. Write the source code to `/home/user/mc_spectroscopy.c`.
2. The program must read an existing file `/home/user/baseline.txt` which contains exactly 100 floating-point numbers (one per line). These represent raw intensity values for 100 spectral bins.
3. Normalize these 100 values so they sum to 1.0. This forms the baseline probability distribution, $Q$.
4. Run a Monte Carlo simulation of 10,000 photon arrival events:
   - Initialize the random number generator strictly with `srand(42)`.
   - For each of the 10,000 events, generate a random probability `r = (double)rand() / RAND_MAX`.
   - Find the first bin index `j` (from 0 to 99) where the cumulative probability of $Q$ (summing from $Q[0]$ to $Q[j]$) is greater than or equal to `r`.
   - Increment a hit counter for bin `j`.
5. Convert the resulting hit counts into an empirical probability distribution $P$ by dividing each bin's count by 10,000.
6. To avoid zero-probabilities in our distance metric, apply a small smoothing factor: add exactly `1e-6` to all 100 bins of both $P$ and $Q$.
7. Re-normalize both $P$ and $Q$ so they each sum to 1.0 again.
8. Compute the Kullback-Leibler divergence from $Q$ to $P$: $D_{KL}(P || Q) = \sum_{i=0}^{99} P_i \ln(P_i / Q_i)$. Use the natural logarithm.
9. Write the computed KL divergence to a log file located at `/home/user/mc_regression.log` in the exact format: `KL: <value>` (use `%.6f` for formatting the float).

Compile and run your program to generate the required log file. Make sure to link the math library.