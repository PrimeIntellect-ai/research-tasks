You are acting as a data scientist analyzing time-resolved spectroscopy data. Our lab uses a custom C-based numerical library called `specfit` to perform fast integrations on raw sensor data, but the latest version we were given seems to be failing its regression tests and producing mathematically incorrect results.

Your task consists of three parts:

**Part 1: Fix the Vendored Package**
A vendored copy of the `specfit` package is located at `/app/specfit-2.1.0`. 
1. Build the package and run its test suite using the provided `Makefile` (`make` and `make test`).
2. You will notice the numerical integration regression tests fail. Diagnose and fix the underlying bug in the C source code (hint: look at how the numerical integration step sizes are handled in `src/integrate.c`).
3. Ensure that `make test` passes completely after your fix.
4. Install the package or compile it so it can be called from your preferred language (a shared library `libspecfit.so` is produced, with a simple C header `specfit.h`).

**Part 2: Signal Processing & Numerical Integration**
We have a dataset at `/home/user/data/spectra_time_series.csv`. 
- The first column is `time` (in milliseconds).
- The remaining columns represent intensity measurements at 500 linearly spaced wavelengths between 400 nm and 800 nm.
- Read this data. For each time step, use the fixed `specfit` library (specifically the `trapz_integrate` function exposed in the library) to compute the total peak area (integral of intensity with respect to wavelength) strictly within the wavelength range of **550 nm to 650 nm** inclusive. 

**Part 3: Model Fitting & Bootstrap Confidence Intervals**
The integrated peak area $A(t)$ decays over time.
1. Fit the extracted areas to the exponential decay model: 
   $A(t) = A_0 e^{-k t} + C$
   Ensure your fitting process is numerically stable.
2. We need robust error bounds on the decay rate $k$. Implement a bootstrap resampling procedure (resampling the *residuals* of your fit) with $N=2000$ iterations to compute the 95% confidence interval for the parameter $k$.
3. Compute the `fitted_areas`, which is the array of $A(t)$ values predicted by your optimized parameters at each time step in the dataset.

**Output Generation**
Save your final analysis to `/home/user/analysis_output.json` with the following exact structure:
```json
{
  "k_mean": 0.0000,
  "k_ci_lower": 0.0000,
  "k_ci_upper": 0.0000,
  "fitted_areas": [0.0, 0.0, ...]
}
```
*Note: The `fitted_areas` list must have the same length as the number of time steps in the CSV, preserving the time order.*