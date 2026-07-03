You are tasked with building a data processing pipeline for a Configuration Management tracking system. The system ingests logs of server configuration changes, calculates rolling statistics to detect anomalous diff sizes, and masks sensitive information before the logs are archived.

You have been provided with a local vendored package that calculates rolling statistics, located at `/app/vendored/py-rolling-stats-0.1.0`. However, the package has a known bug related to its environment variable configuration that prevents it from working correctly.

Your objectives:

1. **Fix and Install the Vendored Package**:
   Navigate to `/app/vendored/py-rolling-stats-0.1.0`. Find the typo in `calculator.py` where it reads the window size from the environment variable (it is misspelled). Fix the bug so it correctly reads `MAX_WINDOW_SIZE`. Install the package in your environment (e.g., using `pip install -e .`).

2. **Develop the Processor Script**:
   Write a Python script at `/home/user/process_configs.py` that processes a directory of JSONL (JSON Lines) files and writes the processed files to an output directory.
   The script must be executable like this:
   `python3 /home/user/process_configs.py <input_dir> <output_dir>`

   Each input JSONL file contains configuration change events. Example line:
   `{"timestamp": "2023-10-01T10:00:00Z", "server_id": "srv-01", "diff_size": 25, "content": "host=192.168.1.10\npassword=superSecret"}`

3. **Data Processing Requirements**:
   For each line in each file, your script must:
   - **Rolling Statistics & Validation**: Use the installed `py_rolling_stats.RollingCalculator` to maintain a rolling average of `diff_size` *per `server_id`*. You must ensure the environment variable `MAX_WINDOW_SIZE` is set to `5` when running the calculator.
   - If the rolling average of `diff_size` (including the current event) is strictly greater than `50.0`, add a new key `"anomaly": true` to the JSON object. Otherwise, set `"anomaly": false`.
   - **Data Masking (Regex)**: Modify the `"content"` string to redact sensitive data:
     - Replace any IPv4 address (e.g., `192.168.1.1`, `10.0.0.5`) with the exact string `[IPV4]`.
     - Replace any AWS Access Key ID (the exact string `AKIA` followed by exactly 16 uppercase letters or digits) with `[AWS_KEY]`.
     - Replace any password assignment value with `[PASSWORD]`. Specifically, match `password=` followed by any non-whitespace characters, and replace the value (e.g., `password=secret123` becomes `password=[PASSWORD]`). Also match JSON style `"password": "some_value"` and replace it with `"password": "[PASSWORD]"`.

4. **Preservation**:
   Any file that does not contain anomalies or sensitive data must be output with `"anomaly": false` and its `"content"` completely unchanged. Output files must have the same names as the input files.

Ensure your script is robust and correctly handles the regex replacements and rolling state per server.