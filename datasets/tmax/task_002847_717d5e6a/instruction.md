You are a scientific computing assistant helping a researcher debug and analyze a parallel simulation.

The researcher has written a C++ simulation (`/home/user/sim/simulation.cpp`) that generates a time-series signal. However, the simulation produces slightly different, non-reproducible global sum results on each run due to a race condition in the OpenMP parallel loop calculating the sum of the signal. 

Your task is to:
1. Fix the C++ code in `/home/user/sim/simulation.cpp` so that it safely and efficiently computes the `global_sum` using an OpenMP `reduction` clause, ensuring reproducibility and correctness without race conditions.
2. Compile the fixed C++ code using `g++ -O2 -fopenmp simulation.cpp -o simulation` and run it. It will output `signal.txt` (containing the time-series data, one value per line) and `sum.txt` (containing the global sum).
3. Write a Python script `/home/user/sim/analyze.py` to process `signal.txt`. The sampling rate is 1000 Hz.
4. In your Python script, use Fourier analysis (`scipy.fft` or `numpy.fft`) to identify the single most dominant frequency (in Hz) in the signal.
5. Extract the residuals by subtracting the idealized dominant frequency sine wave (using the amplitude and phase derived from the FFT) from the original signal.
6. Perform a Kolmogorov-Smirnov (KS) test (`scipy.stats.kstest`) comparing the residuals to a standard normal distribution (`norm`).
7. Save the analysis results to `/home/user/sim/results.json` with the exact following keys:
   - `"global_sum"`: (float) the value from `sum.txt`
   - `"dominant_freq"`: (float) the dominant frequency in Hz
   - `"ks_statistic"`: (float) the KS test statistic
   - `"p_value"`: (float) the KS test p-value

Please ensure the JSON file is correctly formatted. Do not change the random seed or signal generation parameters in the C++ code, only fix the OpenMP reduction.