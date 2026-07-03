You are a data scientist analyzing decay data from a chemical reactor. Recently, a sensor malfunctioned during several experimental trials. The malfunction acts like a numerical integrator with a wrong step-size adaptation, causing the recorded concentration values to artificially diverge to very high values near the end of the run.

You have been provided with a dataset at `/home/user/reactor_data.csv` containing observational data in three columns: `trial_id`, `time`, and `concentration`. 

Your task is to write a Python script that performs the following end-to-end analysis:

1. **Data Reshaping & Cleaning:** Read the dataset. Identify and completely remove any `trial_id` where the `concentration` exceeds `15.0` at any point during its run (these are the divergent anomaly trials).
2. **Curve Fitting:** For each remaining *valid* trial, fit the exponential decay model $C(t) = A e^{-k t}$ to extract the decay rate parameter $k$ and the amplitude $A$. Use non-linear least squares.
3. **Probability Distribution Distance:** Calculate the Kolmogorov-Smirnov (KS) statistic (using `scipy.stats.kstest`) to compare the empirical distribution of your extracted $k$ values against a theoretical Normal distribution with mean $\mu=0.55$ and standard deviation $\sigma=0.05$.
4. **Statistical Hypothesis Comparison:** Perform a 1-sample t-test (using `scipy.stats.ttest_1samp`) comparing your extracted $k$ values against an expected historical decay rate of `0.50`.
5. **Experimental Data Visualization:** Create a scatter plot of `time` vs `concentration` for all valid data points (across all valid trials). Overlay a single solid line representing the "average fitted curve", which should use the mean of all extracted $A$ values and the mean of all extracted $k$ values. Save this plot to `/home/user/fit_plot.png`.
6. **Result Logging:** Save a JSON file at `/home/user/analysis_results.json` containing the statistical results. The JSON must have exactly the following keys:
   - `"valid_trials_count"`: The number of trials remaining after filtering (integer).
   - `"mean_k"`: The mean of the extracted $k$ values across valid trials (float, rounded to 4 decimal places).
   - `"ks_statistic"`: The KS statistic (float, rounded to 4 decimal places).
   - `"ttest_pvalue"`: The p-value from the 1-sample t-test (float, rounded to 4 decimal places).

You will likely need to install dependencies such as `pandas`, `scipy`, `numpy`, and `matplotlib`. Use standard bash tools and Python to achieve this.