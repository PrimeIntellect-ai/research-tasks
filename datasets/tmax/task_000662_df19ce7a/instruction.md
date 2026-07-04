You are a data scientist working on fitting models and estimating confidence intervals for a new set of experimental observations.

You have been provided with two files:
1. `/home/user/data.txt`: Contains 100 floating-point numbers representing our experimental observations, one per line.
2. `/home/user/indices.txt`: Contains 10,000 lines. Each line contains 100 space-separated integers (ranging from 0 to 99). These represent pre-generated random resampling indices for a bootstrap analysis.

Your task is to write a deterministic bootstrap confidence interval calculator using C++ and standard Linux shell commands.

Step 1: Write a C++ program at `/home/user/bootstrap.cpp`.
- It must read `data.txt` into an array/vector.
- It must read `indices.txt`. For each of the 10,000 lines, it should calculate the mean of the 100 observations from `data.txt` corresponding to the indices on that line.
- You must use OpenMP (`#pragma omp parallel for`) to parallelize the loop over the 10,000 bootstrap iterations. 
- The program should print the 10,000 computed means to standard output, one per line (in the same order as the lines in `indices.txt`).

Step 2: Create a bash script at `/home/user/run_analysis.sh`.
- The script should compile the C++ program using `g++ -O2 -fopenmp /home/user/bootstrap.cpp -o /home/user/bootstrap_calc`.
- It should run the compiled executable and save the 10,000 means.
- Using standard shell utilities (like `sort`, `sed`, `awk`), the script must reshape/sort the output to find the 95% Bootstrap Confidence Interval. Specifically, since there are 10,000 samples, sort the means numerically and extract the 250th value (lower bound) and the 9750th value (upper bound).
- The script should output these two values into a file named `/home/user/ci.txt` in exactly this format:
```
Lower CI: <value>
Upper CI: <value>
```

Ensure your C++ code avoids race conditions when reading or writing data. Do not execute the bash script directly in your final response; just create the `.cpp` and `.sh` files, but you may test them in your environment to ensure they work.