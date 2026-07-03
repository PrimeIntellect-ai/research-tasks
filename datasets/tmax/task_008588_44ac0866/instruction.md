You are an analyst tasked with evaluating the robustness of a linear relationship between two system metrics. Because our dataset is small, you need to use Bootstrap Sampling to estimate the average Pearson correlation coefficient.

Your task is to write a C program that reads a CSV dataset, performs bootstrap sampling to generate multiple re-samples of the data, calculates the Pearson correlation coefficient for each sample, and outputs the mean of these correlation coefficients.

Here are the exact requirements:

1. **Dataset:** 
   Assume there is a file at `/home/user/data.csv` containing two columns of floating-point numbers separated by a comma (no header). There will be at most 100 rows.

2. **C Program Requirements:**
   - Create a C source file at `/home/user/boot_corr.c`.
   - The program should take exactly two command-line arguments: the path to the CSV file and the number of bootstrap iterations `N` (integer).
   - Read the dataset into memory. Count the number of rows (`num_rows`).
   - Run `N` bootstrap iterations. In each iteration:
     - Create a bootstrap sample of size `num_rows` by sampling *with replacement* from the original dataset.
     - Calculate the Pearson correlation coefficient between the two columns for this sample.
   - Calculate the mean of these `N` correlation coefficients.
   - Print *only* the final mean correlation coefficient to standard output, formatted to exactly four decimal places (e.g., `0.9852`).

3. **Deterministic Sampling (Crucial for Verification):**
   To ensure reproducible results across environments, DO NOT use the standard library `rand()` function, as its implementation varies. Instead, you MUST use the following exact Linear Congruential Generator (LCG) function to generate random indices:

   ```c
   unsigned int seed = 42;
   unsigned int my_rand() {
       seed = (seed * 1103515245 + 12345) & 0x7fffffff;
       return seed;
   }
   ```
   For every single row drawn in a bootstrap iteration, pick the row index (0-indexed) using: `int idx = my_rand() % num_rows;`. 
   Draw the rows sequentially for the sample array (index 0 to `num_rows - 1`). Do this for all `N` iterations. Do NOT reset the seed between iterations.

4. **Execution:**
   - Compile your program: `gcc -O3 -o /home/user/boot_corr /home/user/boot_corr.c -lm`
   - Run it with 1000 iterations and save the output to `/home/user/result.txt`:
     `/home/user/boot_corr /home/user/data.csv 1000 > /home/user/result.txt`

Ensure your calculations handle standard Pearson correlation safely (if a sample happens to have zero variance, you can assume it evaluates to 0 or handle division by zero by skipping, though our dataset is designed to avoid this).