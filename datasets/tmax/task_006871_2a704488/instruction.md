You are acting as a bioinformatics researcher's assistant. Your lab has generated simulated Raman spectroscopy data for a cohort of cells, split into a `control` group and a `treatment` group. The data is located in `/home/user/data/control/` and `/home/user/data/treatment/`.

Your task is to write and execute a Python script (`/home/user/analyze.py`) that performs signal processing, statistical analysis, and visualization on this data.

Requirements for `/home/user/analyze.py`:
1. **Data Loading**: Read all CSV files from both directories. Each CSV contains `wavenumber` and `intensity` columns (wavenumber ranges from 400 to 2000).
2. **Signal Processing**: For every spectrum, apply the following steps in order:
   - Smooth the `intensity` using a Savitzky-Golay filter (`scipy.signal.savgol_filter`) with `window_length=21` and `polyorder=3`.
   - Perform a simple linear baseline correction: subtract a straight line that connects the first and last points of the *smoothed* spectrum.
3. **Feature Extraction**: Extract the maximum intensity value from the processed (smoothed and baseline-corrected) signal within three specific wavenumber windows:
   - Window 1: [480, 520] (Targeting peak at 500)
   - Window 2: [980, 1020] (Targeting peak at 1000)
   - Window 3: [1480, 1520] (Targeting peak at 1500)
4. **Statistical Analysis**: For each of the three windows, perform an independent two-sided t-test (`scipy.stats.ttest_ind` with default equal variance assumption) comparing the maximum peak intensities of the `control` group versus the `treatment` group.
5. **Output 1 - JSON**: Save the p-values of the t-tests into a JSON file at `/home/user/stats.json`. The JSON should be a flat dictionary with keys `"500"`, `"1000"`, and `"1500"` mapping to their respective p-values as floats.
6. **Output 2 - Visualization**: Plot the mean processed spectrum (smoothed and baseline-corrected) for both the Control and Treatment groups on a single figure. Save this plot to `/home/user/mean_spectra.png`.

Ensure your script is fully autonomous, properly handles dependencies, and writes the output files exactly to the specified paths. You may use shell commands to install any required packages like `numpy`, `pandas`, `scipy`, and `matplotlib`.