You are acting as a performance engineer creating a synthetic scientific workload to profile CPU and I/O bottlenecks on a new cluster. 

Your task is to write and execute a benchmark script (in a language of your choice) that combines Monte Carlo signal generation, spectral analysis, analytical validation, and scientific data I/O.

Please implement a script that does the following:
1. Generates $N = 1000$ independent time-series signals. Each signal must be $M = 10000$ samples long, representing a duration of 10 seconds (i.e., a sampling rate $F_s = 1000$ Hz).
2. For each signal $i$, randomly draw a true fundamental frequency $f_{0,i}$ from a Uniform distribution between 50.0 Hz and 150.0 Hz.
3. The signal equation must be: $S_i(t) = \sin(2 \pi f_{0,i} t) + \epsilon(t)$, where $\epsilon(t)$ is Gaussian white noise with mean 0.0 and standard deviation 2.0.
4. Compute the Discrete Fourier Transform (FFT) for each signal to find the peak frequency $f_{peak,i}$ (the positive frequency bin with the maximum magnitude).
5. Analytically validate the result by calculating the Mean Absolute Error (MAE) between the true frequencies $f_{0,i}$ and the detected peak frequencies $f_{peak,i}$ across all 1000 signals.
6. Save the generated data to an HDF5 file at `/home/user/benchmark_data.h5`. The file must contain exactly two datasets at the root level:
   - `signals`: A 2D array of shape `(1000, 10000)` containing the raw time-series data.
   - `peak_frequencies`: A 1D array of shape `(1000,)` containing the detected $f_{peak,i}$ values.
7. Write the calculated MAE to a log file at `/home/user/validation.log`. The file should contain exactly one line with the format: `MAE: <value>` (e.g., `MAE: 0.025`).

Run your script to produce the final `/home/user/benchmark_data.h5` and `/home/user/validation.log` files.