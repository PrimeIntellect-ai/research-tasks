You are a research assistant working on a scientific simulation pipeline. We recently updated our spectroscopy processing algorithms and need to write a C++ regression test to verify that our FFT-based spectral analysis still matches our baseline validation data.

Your task is to write a C++ program that reads synthetic spectroscopy data from an HDF5 file, processes it, performs spectral analysis, and generates a regression test report.

**Details:**
1. **Input Data:** An HDF5 file is located at `/home/user/spectroscopy_data.h5`. It contains two datasets at the root level:
   - `/signal`: A 1D array of 1000 `double` values representing a time-domain signal.
   - `/baseline_peak`: A single `double` value representing the expected dominant frequency in Hz.
   The sampling rate of the signal is $F_s = 1000$ Hz.

2. **C++ Program Requirements:**
   - Create a C++ file at `/home/user/regression_test.cpp`.
   - Read the `/signal` and `/baseline_peak` datasets from the HDF5 file.
   - Apply a Hann window to the signal. The window function is $w[n] = 0.5 \times (1 - \cos(\frac{2\pi n}{N-1}))$, where $N$ is the number of samples (1000).
   - Compute the Fast Fourier Transform (FFT) of the windowed signal. You must use the `fftw3` library.
   - Calculate the power spectrum (magnitude squared of the complex FFT output) for the first half of the spectrum (positive frequencies).
   - Identify the peak frequency (the frequency bin with the maximum power).
   - Compare the calculated peak frequency with the baseline peak frequency read from the HDF5 file. The test passes if the absolute difference is less than 0.5 Hz.

3. **Output:**
   The program must write its results to a file named `/home/user/test_report.txt` exactly in this format:
   ```
   Calculated Peak Frequency: <value> Hz
   Baseline Peak Frequency: <value> Hz
   Regression Test: <PASS or FAIL>
   ```
   *Format the floating-point numbers to exactly 2 decimal places.*

4. **Compilation & Execution:**
   - You must successfully compile and run your code. You can link against HDF5 and FFTW3 using `-lhdf5` and `-lfftw3`.

Ensure that you leave the final `/home/user/test_report.txt` file in place for automated grading.