You are an AI assistant helping a data scientist clean a noisy telemetry dataset using C for high performance. 

You have been provided with a dataset at `/home/user/telemetry.txt`. The file contains a single column of floating-point numbers, representing sequential sensor readings (one per line). There are fewer than 1,000 readings in total.

Your task is to write and execute a C program that processes this data to compute summary statistics, apply a rolling window, and extract normalized features. 

Specifically, your C program must:
1. Read all the floating-point values from `/home/user/telemetry.txt` into memory. Use `double` precision for all calculations.
2. **Summary Statistics:** Compute the global mean and population standard deviation of the entire dataset.
3. **Rolling Statistics & Feature Extraction:** For every data point starting from the 3rd element (index 2), compute:
    * The **3-element rolling mean** (the average of the current element and the two immediately preceding elements).
    * The **Z-score** of the current element, calculated using the global mean and global population standard deviation you computed in step 2.

Output Requirements:
1. Write the global statistics to a file at `/home/user/summary.txt` in exactly the following format:
   ```
   Mean: [value]
   StdDev: [value]
   ```
   Format the numbers to exactly 4 decimal places (e.g., `%.4f`).

2. Write the processed time-series data to a CSV file at `/home/user/processed.csv`. For each element starting from the 3rd element (index 2), write a row with the following columns:
   `raw_value,rolling_mean,z_score`
   Format all numbers to exactly 4 decimal places.

Do not use any external C libraries other than the standard library (`stdio.h`, `stdlib.h`, `math.h`, etc.). Compile and run your program to produce the final output files.