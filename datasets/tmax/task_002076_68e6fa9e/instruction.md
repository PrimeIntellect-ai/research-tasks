You are a data scientist validating a theoretical physical model for particle emission intervals using a multi-language pipeline. You have been provided with an experimental dataset of emission intervals.

Your task spans environment management, analytical model fitting (Python), distribution validation, and visualization (R).

**Phase 1: Environment Setup**
Ensure your Python environment has the necessary libraries to perform statistical fitting (`scipy`, `numpy`). You may install them in your user environment. 

**Phase 2: Analytical Model Fitting (Python)**
1. The experimental data is located at `/home/user/data/observations.txt` (one float per line).
2. Write and execute a Python script (`/home/user/workspace/fit_model.py`) that:
   - Reads the experimental data.
   - Fits a Gamma distribution to the data. You must use `scipy.stats.gamma.fit` and force the location parameter (`floc`) to `0`.
   - Extracts the fitted `shape` (often denoted as `a`) and `scale` parameters.
   - Writes these parameters to `/home/user/workspace/params.csv` with a header `shape,scale` and the corresponding fitted values on the second line (comma-separated).

**Phase 3: Validation and Visualization (R)**
1. Write and execute an R script (`/home/user/workspace/validate.R`) that:
   - Reads the original data from `observations.txt` and the parameters from `params.csv`.
   - Computes the Kolmogorov-Smirnov (KS) distance metric between the empirical experimental data and the analytical Gamma distribution defined by your fitted parameters. Use R's built-in `ks.test` function (comparing the data against `pgamma`).
   - Extracts the KS test statistic ($D$).
   - Writes ONLY the test statistic rounded to 4 decimal places to a file at `/home/user/workspace/ks_stat.txt`.
   - Generates a plot saving it as `/home/user/workspace/cdf_plot.png` (800x600 pixels). The plot must contain the Empirical Cumulative Distribution Function (ECDF) of the observations (using base R `ecdf`) and overlay the analytical Cumulative Distribution Function curve of the fitted Gamma distribution.

Constraints:
- Do not use root privileges. Use standard user paths.
- All code must be runnable in a standard Linux terminal without graphical desktop interaction.