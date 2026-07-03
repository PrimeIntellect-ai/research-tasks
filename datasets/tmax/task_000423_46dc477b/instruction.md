I need you to write a high-performance C program to analyze sensor data from a CSV file. The file is located at `/home/user/sensor_data.csv` and contains four columns: `timestamp,sensor_id,temperature,status`. 

Your task is to calculate the 95% confidence interval for the mean `temperature` using a bootstrap sampling approach. 

Here are the exact requirements:
1. **Data Parsing (Tokenization) & Missing Values**: Write a C program `bootstrap_ci.c` (saved in `/home/user/`) that reads `/home/user/sensor_data.csv`. Skip the header row. The `temperature` column is the 3rd column. You must handle missing values: ignore any row where the temperature field is empty (e.g., `,,`) or exactly the string `NA`. 
2. **Bootstrap Sampling**: Store the valid temperature values as `double`s. Perform `B = 10000` bootstrap resamples. A bootstrap resample is created by drawing `N` samples with replacement from the original valid dataset (where `N` is the number of valid rows). Calculate the mean of each of the 10000 resamples.
3. **Random Number Generator**: To ensure deterministic and verifiable results, DO NOT use standard `rand()`. Implement and use this exact Linear Congruential Generator (LCG) for drawing random indices:
   ```c
   unsigned int seed = 42;
   unsigned int my_rand() {
       seed = (seed * 1103515245 + 12345) & 0x7fffffff;
       return seed;
   }
   ```
   To pick a random index `i` from `0` to `N-1`, use `int idx = my_rand() % N;`. Note: Draw indices in order for each bootstrap sample (i.e., sample 0 to N-1 for bootstrap 1, then sample 0 to N-1 for bootstrap 2, etc.).
4. **Evaluation**: After generating the 10000 bootstrap means, calculate the grand mean of the *original* valid dataset. Then, sort the 10000 bootstrap means in ascending order to find the 95% confidence interval using the percentile method. The lower bound is the 2.5th percentile (index 250) and the upper bound is the 97.5th percentile (index 9750).
5. **Output**: Write the results to `/home/user/result.json` in exactly this format:
   ```json
   {
     "original_mean": 25.12,
     "ci_lower": 24.85,
     "ci_upper": 25.30
   }
   ```
   Format all numbers to exactly 2 decimal places.

Compile your program to `/home/user/bootstrap_ci` using `gcc` and standard libraries only (`-lm` is allowed), and then run it to generate the JSON file.