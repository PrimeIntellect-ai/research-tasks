You are a data engineer building a high-performance ETL pipeline to detect anomalies in sensor telemetry. 

You have been provided with a raw, multi-gigabyte dataset at `/data/telemetry.csv` containing historical readings. The CSV has the following schema:
`timestamp,sensor_id,diagnostic_payload,reading`

The `diagnostic_payload` field is enclosed in double quotes and occasionally contains embedded newline (`\n`) characters.

You also have a proprietary anomaly detection tool located at `/app/analyzer`. This tool reads a CSV from standard input and outputs detected anomalies to standard output (format: `timestamp,sensor_id`). 
However, there's a known issue: `/app/analyzer` is a legacy stripped binary that is not fully RFC 4180 compliant. It silently drops any records containing embedded newlines, which causes the pipeline to miss critical anomalies (false negatives). It also processes data sequentially, which is too slow for our production SLAs.

Your objective is to write a Bash script `/home/user/process.sh` that accomplishes the following:
1. **Data Cleaning**: Pre-process the CSV data to replace any embedded newlines inside the `diagnostic_payload` field with a single space character, ensuring no rows are dropped by the analyzer.
2. **Parallel Processing**: Partition the cleaned data and process it through `/app/analyzer` in parallel (e.g., using `xargs`, `parallel`, or background jobs) to maximize throughput.
3. **Aggregation**: Collect and combine the outputs into a single file at `/home/user/anomalies.csv`, sorted chronologically by `timestamp`.
4. **Logging**: The script must continuously append its progress, including the start and end times of the parallel batches, to `/home/user/pipeline.log`.

Your solution will be evaluated based on the F1-score of the detected anomalies in `/home/user/anomalies.csv` compared to a hidden ground truth dataset. You must achieve an **F1-score >= 0.98**.

Constraints:
- You must write your pipeline orchestration and cleaning logic entirely in Bash (standard GNU utilities like `awk`, `sed`, `parallel` are allowed and encouraged).
- Do not modify `/app/analyzer`.
- Your script must be executable (`chmod +x /home/user/process.sh`).