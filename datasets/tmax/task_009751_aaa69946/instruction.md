You are a machine learning engineer preparing a training dataset for a new model that predicts material properties from raw spectroscopic data. You have been given a set of 100 raw observational spectra, but they are noisy and sampled on non-uniform, uneven sensor grids.

Your task is to write a Python script `/home/user/process_spectra.py` that preprocesses these observations and extracts key features for the ML model. The raw data files are located in `/home/user/spectra/` and are named `spec_000.txt` through `spec_099.txt`. Each file contains comma-separated `wavelength,intensity` pairs on each line.

Your script must perform the following pipeline on every file:
1. **Domain Reshaping (Regridding):** Read the unevenly sampled raw (x, y) data. Use linear interpolation to resample the intensity data onto a new, perfectly uniform "mesh" (grid) of exactly 1000 points ranging from a wavelength of 400.0 to 800.0 (inclusive).
2. **Signal Processing:** Smooth the newly uniformly-gridded intensity data using a Savitzky-Golay filter. You must use `scipy.signal.savgol_filter` with a window length of 51 and a polynomial order of 3.
3. **Curve Fitting:** Fit a standard 1D Gaussian function to the smoothed data to extract the primary peak parameters. The Gaussian function must be defined exactly as: `f(x) = A * exp(-(x - mu)**2 / (2 * sigma**2))`. 
   * Use `scipy.optimize.curve_fit`.
   * To ensure convergence consistency, provide an initial guess of `p0=[10.0, 600.0, 20.0]` for `[A, mu, sigma]`.
4. **Parallel Processing:** You must process these files in parallel to simulate scaling to millions of spectra. Use Python's `multiprocessing.Pool` with exactly 4 worker processes to distribute the workload.

After processing all 100 files, your script must output a CSV file located at `/home/user/features.csv`.
The CSV must have the following exact characteristics:
- A header row exactly matching: `filename,A,mu,sigma`
- One row per processed file, sorted alphabetically by `filename` (e.g., `spec_000.txt`, `spec_001.txt`, etc.).
- The extracted parameters (`A`, `mu`, `sigma`) must be rounded to exactly 2 decimal places.

Run your script to generate the final `/home/user/features.csv`.