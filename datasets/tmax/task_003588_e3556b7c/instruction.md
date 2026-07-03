You are a data scientist tasked with analyzing noisy optical emission spectroscopy data to precisely locate emission peaks and quantify their uncertainties. 

You have been provided with a local, pre-release version of a specialized library called `pyspectro` located at `/app/pyspectro-1.0.0/`. However, the developer mentioned there might be a typo in the package configuration that prevents it from being installed.

Your workflow should be as follows:
1. **Fix and Install the Package**: Investigate the `/app/pyspectro-1.0.0/` directory, find the installation bug, fix it, and install the package into your environment.
2. **Process Spectral Data**: You are provided with a dataset at `/home/user/spectrum_data.csv`. The file contains two columns: `wavelength` (nm) and `intensity` (arbitrary units). The data contains three distinct spectral peaks, but it is heavily corrupted by random noise and a polynomial background baseline.
3. **Bootstrap Confidence Intervals**: 
   - Fit the 3 peaks using the `pyspectro.voigt.fit_spectrum` function (which returns the centers of the peaks).
   - Because the data is noisy, a single fit is insufficient. Implement a residual bootstrap (Monte Carlo resampling) method with at least 500 iterations.
   - For each iteration, add randomly resampled residuals (with replacement) to your best-fit model, and refit the data to find the new peak centers.
4. **Export Results**: Calculate the mean estimated center and the 95% confidence intervals (using the 2.5th and 97.5th percentiles of your bootstrap distribution) for each of the 3 peaks.
   - Save these results to `/home/user/peak_confidence.csv`.
   - The CSV must have exactly this header: `peak_id,center_mean,ci_lower,ci_upper`
   - `peak_id` should be `1`, `2`, and `3` (ordered by increasing wavelength).

**Constraints**:
- Use Python for your data processing and modeling script. 
- You must use the provided `pyspectro` package for fitting the spectrum.
- The automated verification will test your calculated `center_mean` against the hidden ground truth peak centers. Your Mean Absolute Error (MAE) across the 3 peaks must be less than 0.05 nm.