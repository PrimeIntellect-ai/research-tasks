You are a log analyst tasked with investigating and replacing a legacy binary data processing pipeline. 

We have a stripped legacy binary located at `/app/log_oracle`. We have lost its source code, and we need to rewrite it in Go. 

Through some preliminary investigation, we know the following about what the oracle does:
1. It reads CSV data from standard input with the header: `timestamp,message,metric`
2. It suffers from a known parsing quirk: it silently completely drops any row that contains an embedded newline (`\n`) anywhere within its fields.
3. It performs hash-based deduplication: it calculates the MD5 hash of the `message` string. If a message with the same MD5 hash has been seen previously in the input, the row is discarded.
4. It performs resampling and gap-filling: It groups the remaining valid rows into 10-second buckets based on the `timestamp` (e.g., timestamps 100 to 109 fall into bucket 100). It finds the minimum and maximum bucket timestamps from the valid data. For every 10-second bucket between the minimum and maximum (inclusive), it calculates the sum of the `metric` values. If a bucket has no data, its sum is 0.
5. It performs anomaly detection: It outputs a boolean anomaly flag (represented as `1` or `0`). An anomaly is flagged `1` if the current bucket's sum of `metric` is strictly greater than the previous bucket's sum plus 50. The very first bucket in the output always has an anomaly flag of `0`.
6. It writes the result to standard output in CSV format with the header: `bucket,sum,anomaly`

Your task is to write a Go program at `/home/user/solution.go` and compile it to an executable at `/home/user/solution`.
Your program must replicate the behavior of `/app/log_oracle` EXACTLY. It will be verified against the oracle by feeding both programs with a wide variety of fuzzed CSV inputs and ensuring their standard outputs are bit-for-bit identical. 

You can run `/app/log_oracle` and test your implementation with various inputs to ensure edge cases are handled identically.

Requirements:
- Your final compiled program must be at `/home/user/solution`.
- It must read from `os.Stdin` and write to `os.Stdout`.
- Ensure you handle cases where there are no valid rows left after filtering (it should likely output nothing, but verify with the oracle).