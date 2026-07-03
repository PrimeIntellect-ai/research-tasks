You are a performance engineer profiling a microservice. You have been given a raw application log file located at `/home/user/app_profile.log`. The file contains various interleaved log messages, some of which record request latencies.

Your goal is to parse these latencies, fit a statistical distribution, and determine how many samples are required for your parameter estimates to converge. 

Please complete the following steps:
1. **Data Reshaping**: Parse `/home/user/app_profile.log` and extract all latency values. They are found in lines matching the pattern `Latency: <value> ms`. Ignore all other log lines. Preserve the original top-to-bottom order of the extracted latencies. Let the total number of extracted latencies be $N$.
2. **Distribution Fitting**: Assuming the latency data follows an Exponential distribution, estimate its rate parameter $\lambda$. (Recall that for an Exponential distribution, the Maximum Likelihood Estimate for $\lambda$ is $1 / \mu$, where $\mu$ is the sample mean). Calculate the overall $\lambda$ using all $N$ samples.
3. **Convergence Testing**: We want to know how quickly the sample mean stabilizes. Evaluate the sample mean using only the first $k$ samples, for $k \in \{50, 100, 150, 200, \dots, N\}$ (i.e., step sizes of 50). Find the *smallest* $k$ such that for **all** evaluated sample sizes $j \ge k$ (where $j$ is a multiple of 50), the sample mean of the first $j$ samples is within $\pm 1\%$ of the overall sample mean (inclusive).
   - Condition: `abs(mean_j - overall_mean) <= 0.01 * overall_mean`

Write your final results to a JSON file at `/home/user/profiling_results.json` with the following exact keys and format:
- `"total_samples"`: (integer) The total number of valid latency samples extracted ($N$).
- `"overall_lambda"`: (float) The estimated $\lambda$ using all $N$ samples, rounded to 4 decimal places.
- `"convergence_k"`: (integer) The minimum sample size $k$ satisfying the convergence criteria described above.

You may use any programming language (Python, bash, awk, etc.) to accomplish this task.