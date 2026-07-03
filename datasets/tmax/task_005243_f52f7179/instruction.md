You are a performance engineer analyzing a new candidate release of a microservices backend. 
You have two profiling datasets: `/home/user/baseline.csv` (Release A) and `/home/user/candidate.csv` (Release B).

Each CSV file contains multi-dimensional performance metrics recorded over 100 runs for several API endpoints.
The CSV header is: `endpoint_id,run_id,cpu_time_ms,mem_usage_mb,disk_io_kb`

Your goal is to write a bash script, `/home/user/analyze_perf.sh`, that identifies endpoints where `cpu_time_ms` has statistically degraded in the candidate release. 

Specifically, your script must:
1. Parse both CSV files.
2. For each `endpoint_id`, compute the sample mean ($\mu$) and sample variance ($s^2$) of the `cpu_time_ms` for both the baseline ($A$) and the candidate ($B$). (Use $N-1$ for sample variance).
3. Compute the Welch's t-statistic (or Z-score equivalent for large samples) for the difference in means:
   $$Z = \frac{\mu_B - \mu_A}{\sqrt{\frac{s_A^2}{N_A} + \frac{s_B^2}{N_B}}}$$
   where $N_A$ and $N_B$ are the number of runs for that endpoint in baseline and candidate datasets, respectively.
4. Identify endpoints that have significantly degraded. An endpoint is considered "degraded" if:
   - $\mu_B > \mu_A$
   - $Z > 2.58$ (which roughly corresponds to a 99% confidence level)
5. Output the degraded `endpoint_id`s, one per line, sorted in ascending numerical order, to a file named `/home/user/degraded_endpoints.log`.

Requirements & Constraints:
- Use standard Linux utilities (`awk`, `bc`, `bash`, `sort`, etc.) or Python embedded in your bash script to handle the multidimensional array manipulation and numerical calculations.
- Ensure your variance calculation is numerically stable (be careful with floating-point precision if computing sums of squares natively in awk).
- The final output file `/home/user/degraded_endpoints.log` must contain only the integer `endpoint_id`s.

Once you have written and executed your script, the presence and correct contents of `/home/user/degraded_endpoints.log` will be verified.