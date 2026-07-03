You are a data analyst troubleshooting a performance regression pipeline. 

We need to implement a pipeline reproducibility test to verify that our server metrics do not show a severe correlation between CPU usage and latency.

Write a Go program at `/home/user/analyze.go` that performs the following steps:
1. Reads a CSV file located at `/home/user/data.csv`. The CSV has headers, including `cpu` and `latency` (both containing floating-point numbers).
2. Computes the SHA-256 hash of the exact contents of `/home/user/data.csv` to ensure reproducibility.
3. Calculates the Pearson correlation coefficient between the `cpu` column and the `latency` column.
4. Evaluates the test: If the correlation coefficient is STRICTLY LESS than `0.700`, the status is `"PASS"`. Otherwise, it is `"FAIL"`.
5. Writes the result to `/home/user/report.json` in the exact following JSON format (formatting matters):
`{"file_hash": "<sha256_hex_string>", "correlation": <correlation_value_rounded_to_3_decimal_places>, "status": "<PASS_or_FAIL>"}`

Compile and run your Go script to produce the `/home/user/report.json` file. Ensure the Go code handles standard CSV reading, calculates the math properly, and outputs valid JSON.

Notes:
- The correlation value in the JSON should be a float rounded to exactly 3 decimal places (e.g., `0.985`).
- You may use the standard Go library; no external dependencies (like third-party math/stats libraries) are permitted. You must calculate the Pearson correlation from scratch or using standard packages.