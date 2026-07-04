You are a data engineer tasked with fixing and optimizing an ETL pipeline that processes API access logs. 

We have a custom C-based log aggregator located in `/app/fastlog_etl-1.0.0`. It reads a CSV file containing `timestamp,endpoint,latency_ms`, sorts the records by endpoint, groups them, and calculates the total count and average latency per endpoint. 

Currently, the tool is extremely slow. Your investigation reveals two issues:
1. The tool uses a highly inefficient $O(N^2)$ sorting algorithm in its source code before aggregating.
2. The `Makefile` is misconfigured, preventing compiler optimizations.

Your tasks:
1. **Fix the Vendored Package:**
   - Navigate to `/app/fastlog_etl-1.0.0`.
   - Modify `src/process.c` to replace the naive `bubble_sort` with the standard C library's `qsort`. 
   - Fix the `Makefile` to use the `-O3` optimization flag instead of `-O0`.
   - Recompile the tool (it will generate the binary `fastlog_etl` in the `bin/` directory).

2. **Process the Data:**
   - Run the optimized binary on the data file located at `/home/user/api_logs.csv`. 
   - Save the raw CSV output (format: `endpoint,count,avg_latency`) to `/home/user/summary.csv`.
   - Ensure the execution time of the `fastlog_etl` tool is strictly under **1.0 second**. (The unoptimized version takes over 30 seconds).

3. **Generate a Report:**
   - Write a Bash/AWK script that reads `/home/user/summary.csv` and generates an HTML report at `/home/user/report.html`.
   - The HTML file MUST exactly match this template structure:
     ```html
     <html>
     <body>
       <h1>ETL Pipeline Report</h1>
       <ul>
         <li>Endpoint: /api/v1/users | Count: [COUNT] | Avg Latency: [AVG]ms</li>
         <!-- Repeat for each endpoint, keeping the same order as the CSV -->
       </ul>
     </body>
     </html>
     ```

4. **Pipeline Logging:**
   - Create a log file at `/home/user/pipeline.log` that contains exactly two lines:
     `[INFO] ETL extraction completed successfully.`
     `[INFO] HTML report generated.`