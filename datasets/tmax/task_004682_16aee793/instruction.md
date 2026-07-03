You are a data scientist working on a spectral analysis pipeline. The simulation outputs large sets of noisy time-series data, and we need to compute the total spectral power across all signals. However, due to floating-point reduction order issues and precision loss when simply accumulating millions of float values, previous scripts have produced non-reproducible results.

Your task is to write a robust C program to compute the exact total power, and a Python script to visualize the data.

**Requirements:**

1. **Environment Setup:**
   Ensure you have the necessary development libraries installed for HDF5 and FFTW3, as well as Python libraries `h5py`, `numpy`, and `matplotlib`.

2. **C Program (`/home/user/process_signals.c`):**
   - Read the dataset `"signals"` from the HDF5 file located at `/home/user/data/signals.h5`. The dataset has a shape of `(1000, 1024)` and contains 32-bit floats.
   - For each of the 1000 signals (processed in order from index 0 to 999):
     - Apply a Hanning window to the 1024 elements: $w(n) = 0.5 \times (1 - \cos(\frac{2 \pi n}{1023}))$ for $n = 0 \dots 1023$.
     - Compute the 1D real-to-complex Fast Fourier Transform using FFTW3 (specifically, `fftwf_plan_dft_r2c_1d`).
     - Calculate the power of each frequency bin $k$ (for $k = 0 \dots 512$) as $P(k) = \text{Re}[X_k]^2 + \text{Im}[X_k]^2$.
   - Accumulate the power $P(k)$ for all frequency bins and all signals into a single total sum. 
   - **Crucial:** To prevent floating-point precision loss, you must accumulate the sum using **Kahan summation** with `double` precision variables. Accumulate bin by bin (0 to 512), then signal by signal (0 to 999).
   - Write the final sum to `/home/user/total_power.txt` in the exact format: `Total Power: <value>` (rounded to 6 decimal places).

3. **Visualization (`/home/user/plot_spectrum.py`):**
   - Write a Python script that reads the same HDF5 file.
   - Calculates the mean power spectrum across all 1000 signals (using the same Hanning window and real FFT).
   - Saves a plot of the mean power spectrum (Frequency Bin on X-axis, Mean Power on Y-axis) to `/home/user/mean_spectrum.png`.

Compile and run your C program, and execute your Python script to generate the required outputs.