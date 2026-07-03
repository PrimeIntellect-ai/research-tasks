You are a bioinformatics analyst processing observational DNA sequence data. You have been given a dataset of sequence fragments and need to identify hidden periodicities using spectral analysis, while establishing statistical significance via Monte Carlo permutations.

The input data is located at `/home/user/sequences.csv` and contains three columns: `batch_id`, `recorded_at`, and `sequence`.

Your task is to write and execute a Python script that performs the following steps:
1. **Reshape and Map**: Read the CSV file. Sort the rows chronologically by the `recorded_at` column. Concatenate all the `sequence` strings in this sorted order into one single, continuous string. Convert this string into a 1D numerical array using the following mapping: `A = 1`, `C = 2`, `G = 3`, `T = 4`.
2. **Spectral Analysis**: Compute the Power Spectral Density (PSD) of the full numerical array using a standard Fast Fourier Transform (FFT). The PSD is defined here as the squared magnitude of the FFT output (`abs(fft(x))**2`). 
3. **Peak Detection**: Ignoring the DC component (index 0), find the index and value of the maximum PSD peak.
4. **Monte Carlo Simulation**: To determine if this peak is statistically significant, establish a baseline. Set the random seed strictly using `numpy.random.seed(42)`. Perform 1000 iterations where you:
   - Randomly permute the full numerical array (e.g., using `numpy.random.permutation`).
   - Calculate the PSD of the shuffled array (again, ignoring index 0).
   - Record the maximum PSD value of this shuffled array.
5. **Threshold Calculation**: Calculate the 95th percentile of these 1000 maximum PSD values.
6. **Output**: Write the results to a JSON file at `/home/user/spectral_analysis.json` with the following exact keys and types:
   - `"max_psd_index"`: integer index of the maximum PSD value.
   - `"max_psd_value"`: float of the maximum PSD value, rounded to 2 decimal places.
   - `"mc_threshold_95"`: float of the 95th percentile threshold from the Monte Carlo simulation, rounded to 2 decimal places.

Ensure you install any necessary Python packages (like `pandas` and `numpy`) using `pip` before running your script.