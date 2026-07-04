You are a log analyst investigating network latency patterns across several servers. You have received a batch of log data, but it requires cleaning, reshaping, and summarization before it can be shared with the DevOps team.

Your task is to create a C++ pipeline that processes this data.

**System State & Requirements:**
1. There is a raw log file located at `/home/user/raw_metrics.csv`. This file is encoded in **UTF-16LE** and contains a header followed by latency metrics in a "wide" format: `Timestamp,ServerAlpha,ServerBeta,ServerGamma`.
2. There is a report template file at `/home/user/report_template.txt`. 

**Objective:**
Write a C++ program (and any necessary shell commands to compile and run it) to perform the following:
1. **Encoding Handling:** Safely read the UTF-16LE `raw_metrics.csv` file (you may use shell utilities like `iconv` to convert it to UTF-8 before passing it to your C++ program, or handle it natively).
2. **Reshaping:** Convert the data from the wide format (`Timestamp, ServerAlpha, ServerBeta, ServerGamma`) into a long format internally (`Timestamp, ServerName, MetricValue`).
3. **Data Validation:** Discard any log entries (specific metric values) that violate the physical constraints of our network: Latency must be `>= 0.0` and `<= 1000.0`. Do not discard the whole row, just the specific invalid metric for that server at that timestamp.
4. **Aggregation:** Calculate the mean latency for each server based only on the valid data points.
5. **Report Generation:** Read `/home/user/report_template.txt`. Replace the placeholder `{{REPORTS}}` with the formatted averages. Each server's average should be on a new line in the format: `[ServerName]: [Average] ms` (rounded to exactly 2 decimal places).
6. Output the final generated text to `/home/user/final_report.txt`.

**Example internal long data after extraction:**
`1622540000, ServerAlpha, 45.5`

**Example Replacement Text:**
```
ServerAlpha: 45.50 ms
ServerBeta: 102.00 ms
```

Make sure all operations are fully scripted or command-line driven. Install any compiler tools you need via `apt` (e.g., `sudo apt-get update && sudo apt-get install -y g++` if required).