You are a data scientist analyzing output from a continuous particle detector. You have been provided with a CSV file at `/home/user/detector_events.csv` that contains a single column `timestamp` representing the exact time (in seconds) an event was recorded. 

Your task is to perform the following steps using Python:

1. **Observational Data Reshaping**: Load the CSV and compute the inter-arrival times (the time differences $\Delta t$ between consecutive event timestamps). 
2. **Density Estimation & Distribution Fitting**: Fit an exponential distribution to these inter-arrival times. Specifically, estimate the rate parameter $\lambda$ (where $\lambda = 1 / \text{mean}(\Delta t)$).
3. **Analytical Solution Validation**: Validate the fit by calculating the maximum absolute difference between the empirical cumulative distribution function (ECDF) of your $\Delta t$ data and the theoretical CDF of the fitted exponential distribution. This is equivalent to the Kolmogorov-Smirnov (KS) statistic.
4. **Experimental Data Visualization**: Generate a plot containing a histogram of the inter-arrival times (density=True) overlaid with the theoretical probability density function (PDF) of the fitted exponential distribution. Save this plot to `/home/user/fit_plot.png`.
5. **Reporting**: Create a JSON file at `/home/user/fit_results.json` containing your calculated rate parameter and the KS statistic. The JSON must have exactly this structure:
```json
{
  "lambda": 0.0000,
  "ks_stat": 0.0000
}
```
Round both values to 4 decimal places.

Ensure you install any necessary Python packages (like `pandas`, `numpy`, `scipy`, `matplotlib`) using `pip` if they are not already present in your environment.