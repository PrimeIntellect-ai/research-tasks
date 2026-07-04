You are a performance engineer profiling a microservice application. You have collected request latency data (in milliseconds) from the current production version and a newly deployed release candidate. The data is located at:
- `/home/user/baseline_latencies.txt`
- `/home/user/new_latencies.txt`

Your task is to create a Bash script at `/home/user/evaluate_perf.sh` that evaluates whether the new version represents a performance regression. Your script may use standard CLI tools or inline Python/Perl/Ruby to perform the necessary mathematical operations, but the entrypoint must be the Bash script.

The script must perform the following analysis:
1. **Distribution Fitting & Equation Solving**: Assume the latencies follow an Exponential distribution. For both the baseline and new datasets, fit the data by calculating the Maximum Likelihood Estimate (MLE) for the mean (which implies the rate parameter $\lambda = 1/\text{mean}$). Then, analytically solve the Exponential Cumulative Distribution Function (CDF) equation $F(x) = 1 - e^{-\lambda x} = 0.99$ to find the expected 99th percentile (p99) latency for both versions.
2. **Probability Distribution Distance**: Calculate the 1D Wasserstein distance between the raw empirical baseline and new latency datasets.
3. **Regression Testing**: A performance regression is defined as occurring if AND ONLY IF both of these conditions are met:
   - The fitted p99 latency of the new version is strictly greater than the fitted p99 latency of the baseline version.
   - The Wasserstein distance between the datasets is strictly greater than 2.00.

When executed without any arguments, `/home/user/evaluate_perf.sh` must print exactly four lines to standard output in the following format:
```
Baseline p99: <value>
New p99: <value>
Wasserstein: <value>
Regression: <YES|NO>
```
Round all numerical values to exactly two decimal places (e.g., `42.50`). Make sure your Bash script is executable.