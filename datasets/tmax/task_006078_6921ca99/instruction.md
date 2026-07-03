You are a performance engineer working on a parallel numerical simulation in C++.

We have a program located at `/home/user/pi_sim.cpp` that calculates $\pi$ via numerical integration using OpenMP. However, we are facing two critical issues:
1. **Non-reproducibility**: The calculated value of $\pi$ has slight variations between runs due to floating-point addition order caused by an `atomic` pragma.
2. **Poor Performance**: The `atomic` operation creates a massive bottleneck, effectively serializing the accumulation.

Your task is to fix the code, run a performance experiment, and analyze the results:

1. **Fix the C++ Code**: Modify `/home/user/pi_sim.cpp` to remove the `#pragma omp atomic` bottleneck. Use an OpenMP `reduction` clause to safely and deterministically accumulate the `sum` variable. Do not change the total number of steps.
2. **Compile**: Compile the fixed program to `/home/user/pi_sim` using `g++` with the `-O3` and `-fopenmp` flags.
3. **Run Experiments**: Create and execute a bash script at `/home/user/run_experiments.sh` that runs the compiled `pi_sim` executable exactly 100 times. Extract the execution time (in milliseconds) from each run's stdout and append it to a file named `/home/user/times.csv` (one time value per line, no headers).
4. **Statistical Analysis & Visualization**: Write and execute a Python script at `/home/user/analyze.py` that reads `/home/user/times.csv` and performs the following:
   - Uses a bootstrap resampling method (10,000 resamples, random seed = 42) to calculate the 95% confidence interval of the **mean** execution time.
   - Writes the confidence interval to `/home/user/ci.txt` in the exact format: `lower_bound,upper_bound` (rounded to 3 decimal places).
   - Generates a histogram of the original 100 execution times and saves the plot as `/home/user/histogram.png`.

*Note: The C++ program outputs in the format `Pi: <value>, Time: <ms>`. Ensure your data extraction correctly parses out just the numeric time value.*