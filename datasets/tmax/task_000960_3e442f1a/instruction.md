You are a performance engineer analyzing a legacy application's behavior. We need to model how the system latency scales with incoming request load, but we cannot install external dependencies like Python, R, or specialized profiling tools. You must accomplish this using only standard Linux shell tools (Bash, awk, bc, sed, etc.).

There is a raw log file located at `/home/user/perf_logs.txt`. 

Your task is to write a bash script `/home/user/analyze_perf.sh` that performs the following steps when executed:

1. **Observational data reshaping**: Parse `/home/user/perf_logs.txt`. The log lines contain various debug info, but you need to extract the `load` (requests per second) as your $X$ variable, and the `latency` (milliseconds) as your $Y$ variable. Ignore lines that do not contain both load and latency metrics.

2. **Linear equation solving**: Implement Exact Ordinary Least Squares (OLS) linear regression purely in `awk` (or `bc`/`bash`) to find the best-fit line $Y = mX + b$.
   The formulas for the slope $m$ and intercept $b$ are:
   $m = \frac{n(\sum xy) - (\sum x)(\sum y)}{n(\sum x^2) - (\sum x)^2}$
   $b = \frac{\sum y - m(\sum x)}{n}$
   where $n$ is the number of valid data points.

3. **Statistical hypothesis comparison**: Compare your linear model against a baseline "null hypothesis" model. 
   - The null model assumes latency is independent of load, predicting the mean latency ($\bar{Y}$) for all inputs.
   - Calculate the Mean Squared Error (MSE) of your linear model: $MSE_{model} = \frac{1}{n} \sum (Y_i - (mX_i + b))^2$
   - Calculate the MSE of the null model: $MSE_{null} = \frac{1}{n} \sum (Y_i - \bar{Y})^2$

4. **Output formatting**: Your script must generate a JSON file at `/home/user/results.json` containing the calculated metrics. All numerical values must be formatted to exactly 2 decimal places.

The required JSON format is:
```json
{
  "m": "...",
  "b": "...",
  "model_mse": "...",
  "null_mse": "..."
}
```

Constraints:
- You must write the solution in `/home/user/analyze_perf.sh`.
- The script must be executable.
- You must run your script so that `/home/user/results.json` is generated.
- No Python, Perl, or compiled C code. Use Bash, AWK, sed, grep, bc, etc.