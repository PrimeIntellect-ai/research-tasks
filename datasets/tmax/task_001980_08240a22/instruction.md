You are an automation specialist tasked with creating a robust, multi-language time-series data normalization pipeline. We receive unstructured metric logs from global servers. These logs contain timestamps, metric names, and values, but they are polluted with varying Unicode characters, multi-language brackets, and non-ASCII digits (such as Arabic-Indic digits or full-width characters).

Your objective is to fix a vendored extraction library and write a Python script that perfectly standardizes this stream of logs.

**Step 1: Fix the Vendored Package**
We vendor a local package called `i18n_ts_parser` located at `/app/vendored/i18n_ts_parser`. This library is supposed to help extract metrics, but a recent commit introduced a perturbation: its main regex pattern in `/app/vendored/i18n_ts_parser/extractor.py` was hardcoded to only accept ASCII digits (`[0-9]`) for timestamps and values, causing it to fail on internationalized logs. 
You must inspect the package, find the broken regex logic, and patch it so it properly captures any Unicode digit and accepts both standard brackets `[...]` and full-width brackets `【...】`.

**Step 2: Create the Normalization Pipeline**
Write a Python script at `/home/user/parse_metrics.py`. 
This script must:
1. Read lines from standard input (`sys.stdin`).
2. Use the fixed `i18n_ts_parser` to extract the raw timestamp string, the metric name, and the numeric value string.
3. Normalize the extracted timestamp into a strict ISO 8601 UTC string (e.g., `YYYY-MM-DDThh:mm:ssZ`). You can assume all input timestamps are either already UTC (marked with Z) or lack timezone info (assume UTC).
4. Normalize all non-ASCII digits (like `١٢٣` or `４５６`) in the extracted numeric value to standard ASCII digits (`0-9`), preserving decimal points.
5. Output exactly one line to standard output (`sys.stdout`) per successfully parsed input line in the format: `TIMESTAMP,METRIC_NAME,VALUE` (comma-separated).
6. Ignore or drop any line that does not contain a valid metric.

**Examples:**
Input: `【٢٠٢٣-١٠-٠٥T١٤:٣٠:٠٠Z】 ERROR_RATE ٤٥.٥% (サーバー)`
Output: `2023-10-05T14:30:00Z,ERROR_RATE,45.5`

Input: `[2023-10-05T14:35:00Z] CPU_USAGE ９９.９ (高)`
Output: `2023-10-05T14:35:00Z,CPU_USAGE,99.9`

The final script must be executable (`chmod +x /home/user/parse_metrics.py`) and perfectly match our reference implementation. An automated test will pipe thousands of random, multilingual log lines into your script and check if the output is bit-exact equivalent to our reference oracle.