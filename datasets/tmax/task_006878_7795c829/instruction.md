You are a data scientist analyzing a noisy emission spectrum. You need to compare the empirical spectrum against an expected analytical decay model, computing a statistical distance metric and its bootstrap confidence interval. 

Write a C program at `/home/user/compare_spectra.c` that does the following:

1. **Read Empirical Data**: Read exactly 1000 floating-point values from `/home/user/spectrum.txt`. Each line contains one positive value representing the intensity at index `i` (from 0 to 999). 

2. **Analytical Solution**: Generate an expected analytical distribution $Q$ of length 1000, where the unnormalized intensity at index $i$ is given by $q_i = \exp(-i / 200.0)$. Normalize $Q$ such that the sum of all its 1000 elements equals exactly 1.0.

3. **Bootstrap Confidence Interval**: 
   - Initialize the C random number generator exactly once at the start of your `main` function using `srand(42);`.
   - Perform exactly 100 bootstrap iterations. 
   - In each iteration:
     a. Create a bootstrap sample of size 1000 by drawing with replacement from the original empirical data. Use `rand() % 1000` to select indices. Make exactly 1000 calls to `rand()` per iteration, sequentially filling your sample array from index 0 to 999.
     b. Normalize this bootstrap sample so its elements sum to exactly 1.0, creating a probability distribution $P^*$.
     c. Compute the Total Variation Distance (TVD) between $P^*$ and $Q$. The formula is: $TVD = \frac{1}{2} \sum_{i=0}^{999} |P^*_i - Q_i|$.
     d. Store this TVD value.

4. **Calculate Percentiles**:
   - Sort the 100 computed TVD values in ascending order.
   - Extract the 5th percentile (the element at index 4) and the 95th percentile (the element at index 94).

5. **Output**:
   - The program should create and write the result to a file at `/home/user/result.txt` in the exact format: `CI: [lower_bound, upper_bound]`, using the `%f` format specifier (default 6 decimal places) for the float/double values.

Compile and run your program to produce `/home/user/result.txt`. Use standard C libraries (`stdio.h`, `stdlib.h`, `math.h`).