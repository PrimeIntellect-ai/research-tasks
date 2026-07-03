You are an ML Engineer preparing a pipeline for a new dimensionality reduction model. Before passing the data to the modeling team, you need to verify the statistical properties of the raw feature set, specifically its variance-covariance structure.

Your task is to write a C++ program that computes the sample covariance matrix of a dataset and extracts specific linear algebraic properties (the trace and the top-left element) to verify reproducibility.

Here are the specific requirements:
1. There is a dataset located at `/home/user/features.csv`. It contains 5 rows and 3 columns of floating-point numbers, separated by commas.
2. Write a C++ program at `/home/user/compute_cov.cpp`.
3. The program should read `/home/user/features.csv`.
4. It must compute the sample covariance matrix of the features. Remember to:
   - Compute the mean of each column.
   - Center the data by subtracting the column means.
   - Compute the sample covariance matrix (divide by N-1, where N is the number of rows).
5. Calculate the Trace of the covariance matrix (the sum of its diagonal elements, representing the total variance in the dataset).
6. The program must output these exact two values to a file named `/home/user/cov_stats.txt` in the following format:
   ```
   Trace: <value>
   TopLeft: <value>
   ```
   *(Replace `<value>` with the computed numbers, formatted to 2 decimal places).*
7. Compile your program to an executable named `/home/user/compute_cov` using `g++` and run it to produce the output file.

Ensure your C++ code is self-contained and does not rely on external non-standard libraries (like Eigen) – you should implement the basic linear algebra operations using standard C++ structures (e.g., `std::vector`).