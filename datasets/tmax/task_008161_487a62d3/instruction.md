You are a performance engineer investigating periodic latency spikes in a real-time trading application. You have captured a high-frequency latency trace of 1024 consecutive requests. The data is available as a single column of floating-point numbers in `/home/user/perf_trace.txt`.

Your goal is to write a C++ program (`/home/user/analyzer.cpp`) that performs spectral analysis to identify the frequency of the bottleneck and uses bootstrap resampling to establish a confidence interval for the mean latency.

Write and execute the C++ program to do the following:

1. **Spectral Analysis (Fourier Transform):**
   - Read the 1024 latency values.
   - Compute the Discrete Fourier Transform (DFT or FFT) of the data. You may implement a standard Cooley-Tukey FFT or a naive DFT using `std::complex` (since N=1024 is small).
   - Calculate the magnitude of each frequency bin.
   - Find the "Dominant Frequency Bin": the index (from 1 to 511, strictly ignoring the DC component at index 0) that has the highest magnitude.
   - Export the frequency bins (0 to 511) and their magnitudes to `/home/user/spectrum.csv` in the format: `bin,magnitude`. This prepares the experimental data for visualization.

2. **Bootstrap Confidence Interval:**
   - Compute the 95% bootstrap confidence interval for the **mean** of the original 1024-point dataset.
   - Use exactly 10,000 bootstrap resamples.
   - For reproducible results, initialize your random number generator exactly like this:
     `std::mt19937 gen(42);`
     `std::uniform_int_distribution<> dis(0, 1023);`
     (Draw 1024 indices per resample using `dis(gen)`).
   - Calculate the mean of each resample.
   - Sort the 10,000 means and extract the 2.5th percentile and 97.5th percentile (indices 250 and 9749 if 0-indexed).

3. **Reporting:**
   - Write the results to `/home/user/report.txt` in exactly this format:
     ```
     Dominant Frequency Bin: <integer>
     Mean 95% CI: [<lower_bound>, <upper_bound>]
     ```
     (Format the bounds to exactly 3 decimal places).

Compile your C++ program (e.g., `g++ -O3 analyzer.cpp -o analyzer`) and run it to produce the output files.