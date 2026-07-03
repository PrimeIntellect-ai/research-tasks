You are a performance engineer analyzing a distributed application. You have noticed that the application produces slightly non-reproducible results across different runs. You suspect this is due to floating-point reduction order: different threads finish at different times, causing their partial results to be summed in a non-deterministic order, which leads to precision loss.

Your task is to quantify this instability using Monte Carlo simulation and Bootstrap confidence intervals.

You have a raw log file located at `/home/user/app_profile.log`. 

Perform the following steps:
1. **Data Reshaping**: 
   Parse the log file to extract the floating-point values. The log lines look like this:
   `[2023-10-12 10:00:01] INFO Thread-4: partial_metric = 0.00451`
   Ignore any lines that do not contain `partial_metric`. Extract only the numeric values into a 1D array.

2. **Monte Carlo Simulation**:
   Write a Python script to simulate the effect of random addition order on the total sum.
   - Convert your array of extracted values to `numpy.float16` to exaggerate and observe the precision errors.
   - Set the random seed: `numpy.random.seed(42)`
   - Perform a Monte Carlo simulation with exactly `5000` iterations.
   - In each iteration, randomly shuffle the `float16` array (using `numpy.random.shuffle`) and then compute the sequential sum of the array. *Note: You must accumulate the sum using `numpy.sum` on the shuffled `float16` array to accurately simulate the precision loss.*
   - Store the final accumulated sum for each of the 5000 iterations.

3. **Bootstrap Confidence Intervals**:
   Now, analyze the standard deviation of the sums produced by your Monte Carlo simulation.
   - Set the random seed: `numpy.random.seed(123)` (set this immediately before the bootstrap step).
   - Perform a Bootstrap analysis with exactly `2000` resamples on your 5000 simulated sums to find the 95% confidence interval for the *sample standard deviation* (use `ddof=1` for standard deviation).
   - Use the percentile method for the confidence interval.

4. **Reporting**:
   Save your results in a JSON file at `/home/user/stability_report.json` with the following exact keys:
   - `"num_observations"`: The integer number of valid `partial_metric` values extracted.
   - `"mc_mean_sum"`: The mean of your 5000 simulated sums (as a standard float).
   - `"mc_std_dev"`: The sample standard deviation (`ddof=1`) of your 5000 simulated sums (as a standard float).
   - `"bootstrap_std_dev_ci_lower"`: The lower bound of the 95% CI.
   - `"bootstrap_std_dev_ci_upper"`: The upper bound of the 95% CI.

Make sure you install any necessary Python packages (like `numpy`, `scipy`) using `pip` if they are not present. Write your script and run it to produce the required JSON file.