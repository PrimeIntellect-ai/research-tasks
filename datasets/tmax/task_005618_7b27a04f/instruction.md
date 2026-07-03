You are a data engineer tasked with building a lightweight, high-performance ETL pipeline using Rust. 

We have a raw server log file located at `/home/user/raw_logs.txt`. The log file contains millions of simulated request records. Each line is formatted exactly as follows:
`[YYYY-MM-DD HH:MM:SS] <IP_ADDRESS> - <ENDPOINT> - <STATUS_CODE> - <RESPONSE_TIME_MS>ms`
Example:
`[2023-10-12 14:32:01] 192.168.1.10 - /api/v1/login - 200 - 45.2ms`

Your task is to write a Rust program that processes this file to extract performance metrics. 

1. **Setup**: Create a new Rust project named `etl_pipeline` in `/home/user/` (i.e., the manifest should be at `/home/user/etl_pipeline/Cargo.toml`).
2. **Tokenization & Processing**: Read `/home/user/raw_logs.txt` and parse each line to extract the `<ENDPOINT>` and `<RESPONSE_TIME_MS>` fields. Ignore records with a `<STATUS_CODE>` of 500.
3. **Aggregation & Hypothesis Testing (Confidence Intervals)**: Group the data by `<ENDPOINT>`. For each endpoint, compute:
   - Total count of valid requests ($n$)
   - Mean response time ($\bar{x}$)
   - The 95% confidence interval for the mean response time. Use the standard formula: $CI = \bar{x} \pm 1.96 \times \frac{s}{\sqrt{n}}$, where $s$ is the sample standard deviation. (If $n \le 1$, set the CI bounds to the mean).
4. **Storage Management**: The output must be written to a simulated data warehouse directory. Create the directory `/home/user/data_warehouse/` and write the aggregated results to `/home/user/data_warehouse/aggregated_stats.csv`.
5. **Output Format**: The CSV must have the exact header: `endpoint,count,mean,ci_lower,ci_upper`. The rows should be sorted alphabetically by the `endpoint` name. All floating-point numbers (`mean`, `ci_lower`, `ci_upper`) must be rounded to exactly two decimal places.

Compile and run your Rust program so that the final `aggregated_stats.csv` file is generated and populated accurately.