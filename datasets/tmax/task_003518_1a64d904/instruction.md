You are an AI assistant helping a researcher organize and process a dataset.

The researcher has a raw dataset located at `/home/user/dataset.csv`. The file contains 50 rows and 10 columns of comma-separated floating-point numbers (no header).

Your task is to set up the analysis environment and write a C++ program that performs dimensionality reduction (feature selection) and bootstrap sampling. 

Follow these exact steps:

1. **Analysis Environment Setup:**
   Create a directory `/home/user/analysis`. All your code and outputs should be placed here.

2. **Dimensionality Reduction (Feature Selection):**
   Write a C++ program `/home/user/analysis/process.cpp` that first reads `/home/user/dataset.csv`. 
   Calculate the sample variance for each of the 10 columns. Select the 3 columns with the highest variance. 
   Form a reduced dataset (50 rows, 3 columns) containing ONLY these 3 columns, preserving their original relative left-to-right order. 
   *(Note: Use the standard $n-1$ denominator for sample variance, though $n$ vs $n-1$ won't change the relative ranking).*

3. **Bootstrap Sampling:**
   Using the reduced dataset, perform 1000 bootstrap iterations to estimate the mean of each of the 3 selected features.
   To ensure your results are perfectly reproducible and verifiable, you **must** use the following Linear Congruential Generator (LCG) to select row indices (from 0 to 49) with replacement:
   
   ```cpp
   #include <stdint.h>
   uint32_t lcg() {
       static uint32_t state = 42;
       state = (state * 1664525 + 1013904223);
       return state;
   }
   ```
   For each of the 1000 bootstrap iterations (iteration 0 to 999):
   - Draw exactly 50 row indices. For each draw, use `int row_idx = lcg() % 50;`.
   - Calculate the mean of the 3 features for these 50 sampled rows.

4. **Output:**
   The C++ program should write the results to `/home/user/analysis/bootstrap_means.csv`. 
   The file should contain 1000 rows. Each row should contain the 3 bootstrapped means, separated by commas, formatted to exactly 4 decimal places (e.g., `printf("%.4f,%.4f,%.4f\n", m1, m2, m3);` or using `std::setprecision(4) << std::fixed`).

Compile your program (e.g., using `g++ -O3 process.cpp -o process`) and run it so the output file is generated.