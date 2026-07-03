You are a data engineer building the validation stage of an ETL pipeline. You need to process a stream of incoming sensor measurements, compute rolling statistics robustly, and update a Bayesian belief about the underlying true average of the sensors.

You have been provided with a dataset at `/home/user/measurements.csv` containing a single column of floating-point numbers (no header, 10,000 lines).

Write a Go program at `/home/user/process_stream.go` that implements the following requirements:

1. **Robust Online Statistics**: Simulate reading the CSV file as a stream (line by line). To prevent catastrophic cancellation and ensure numerical accuracy, implement **Welford's Online Algorithm** to compute the running sample mean and sample variance. 
2. **Intermediate Logging**: Every 1000 measurements (i.e., at N=1000, 2000, 3000... up to 10000), append a JSON object to a file at `/home/user/welford_stats.jsonl`. 
   The format must exactly match: `{"n": 1000, "mean": 1.234, "variance": 0.567}`.
   Round the `mean` and `variance` values to exactly 3 decimal places.
3. **Bayesian Inference**: Assume the data is drawn from a Normal distribution with a known variance of $\sigma^2 = 1.0$. You are trying to estimate the true unknown population mean $\mu$. 
   Use a Normal conjugate prior for the mean with a prior mean $\mu_0 = 0.0$ and prior variance $\sigma_0^2 = 1.0$.
   Compute the exact analytical Bayesian posterior mean and posterior variance after processing all 10,000 records.
4. **Final Output**: Write the final posterior statistics (at N=10000) to `/home/user/bayesian_posterior.json`.
   The format must exactly match: `{"posterior_mean": 1.23456, "posterior_variance": 0.00012}`.
   Round the final posterior values to exactly 5 decimal places.

Compile and run your Go program to generate the output files. Do not use any third-party Go packages (e.g., no `gonum`); rely only on the Go standard library.