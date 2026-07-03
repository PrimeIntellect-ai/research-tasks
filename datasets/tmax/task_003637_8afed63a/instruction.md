You are a bioinformatics analyst tasked with processing simulated raw nanopore sequencing data. The raw signal data contains electrical current measurements over time, stored in an HDF5 file. Your goal is to write a Python script that analyzes this signal, extracts specific features, and performs parameter estimation. 

First, ensure your environment has the necessary libraries (e.g., `h5py`, `numpy`, `scipy`). 

The input file is located at `/home/user/nanopore_sim.h5` and contains a single 1D dataset named `signal` at the root level of the HDF5 file. 

Write and execute a Python script to perform the following analysis pipeline:

1. **Signal Filtering & Differentiation:**
   - Load the `signal` dataset.
   - Apply a 4th-order Butterworth low-pass filter with a normalized critical frequency of 0.1. Use `scipy.signal.butter` and `scipy.signal.filtfilt` to avoid phase shifts.
   - Calculate the first derivative of the *filtered* signal using central differences (`numpy.gradient`).
   - Identify the number of "event boundaries" (peaks) in the absolute value of this derivative. Use `scipy.signal.find_peaks` with a minimum `height` of 0.05 and a `distance` of 50 samples.

2. **Numerical Integration:**
   - Calculate the total electrical charge (area under the curve) of a specific segment of the **unfiltered** raw signal.
   - Use Simpson's rule (`scipy.integrate.simpson` or `simps`) to integrate the raw signal from index 1000 to exactly 5000 (i.e., `signal[1000:5000]`). 

3. **Non-linear Parameter Estimation (Optimization):**
   - The segment of the **unfiltered** signal from index 2000 to 2500 (i.e., exactly 500 data points) contains a simulated protein translocation event modeled as a Gaussian function superimposed on the baseline.
   - Define a Gaussian function: `f(x) = A * exp(-((x - mu)**2) / (2 * sigma**2))`
   - Use `scipy.optimize.curve_fit` to fit this Gaussian to the extracted 500-point segment. Use an initial guess (`p0`) of `A=4.0`, `mu=250.0`, and `sigma=50.0`. Note that the independent variable `x` for the fit should be an array from 0 to 499 (representing the relative indices of the segment).

Output your final results into a JSON file located precisely at `/home/user/analysis_results.json`. The JSON file must have exactly the following keys and format:
- `"num_events"`: (integer) The number of peaks detected.
- `"integral_value"`: (float) The calculated integral of the raw signal (rounded to 2 decimal places).
- `"gaussian_A"`: (float) The fitted `A` parameter (rounded to 3 decimal places).
- `"gaussian_mu"`: (float) The fitted `mu` parameter (rounded to 3 decimal places).
- `"gaussian_sigma"`: (float) The fitted `sigma` parameter (absolute value, rounded to 3 decimal places).