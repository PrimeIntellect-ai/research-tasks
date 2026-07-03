You are a security log analyst investigating suspicious patterns in a web server access log. You need to build a robust, reproducible data processing pipeline to extract and aggregate threat intelligence from these logs. 

Your environment has a large, raw access log located at `/home/user/access.log`. The log follows the standard combined log format:
`IP - - [Timestamp] "METHOD ENDPOINT HTTP/1.1" STATUS SIZE`

Your task is to build a Data Directed Acyclic Graph (DAG) pipeline using `snakemake` (you will need to install it via pip) and Python. 

Perform the following steps:

1. Create a `Snakefile` in `/home/user/` that defines a pipeline with three rules: `filter_logs`, `extract_features`, and `aggregate_threats`.
2. **Rule 1: filter_logs**
   - Input: `/home/user/access.log`
   - Output: `/home/user/filtered.log`
   - Action: Run a Python script (you must write it, e.g., `filter.py`) that reads the input file **line-by-line (streaming)** to handle potentially massive files without running out of memory. It should write only the lines where the HTTP STATUS code is `4xx` or `5xx` (i.e., >= 400) to the output file.
3. **Rule 2: extract_features**
   - Input: `/home/user/filtered.log`
   - Output: `/home/user/features.csv`
   - Action: Run a Python script (e.g., `extract.py`) that parses the filtered log lines and extracts the IP address, the HTTP method, and the requested endpoint. The script must write these as a CSV file with the exact headers: `ip,method,endpoint`.
4. **Rule 3: aggregate_threats**
   - Input: `/home/user/features.csv`
   - Output: `/home/user/threats.json`
   - Action: Run a Python script (e.g., `aggregate.py`) that reads the CSV file, counts the total number of anomalous requests (the rows) associated with each IP address, and outputs a JSON file mapping the IP addresses (keys) to their integer counts (values).
5. Run your pipeline by executing `snakemake -c 1` in `/home/user/`.

Ensure all file paths are absolute (`/home/user/...`) or correctly resolved relative to the `/home/user/` working directory. Do not leave the final JSON file unformatted or named incorrectly.