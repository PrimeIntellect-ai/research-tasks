You are tasked with building a bash-based data pipeline to analyze configuration drift across a fleet of servers. A monitoring system continuously logs configuration changes to a large pipe-separated file at `/home/user/config_events.log`.

Each line in this file follows the format:
`TIMESTAMP|SERVER_ID|CONFIG_KEY|BYTES_ADDED|BYTES_REMOVED`
(Example: `2023-10-01T10:00:00|srv01|/etc/nginx/nginx.conf|150|20`)

Your goal is to write a bash script located at `/home/user/process_configs.sh` that processes this log file using standard CLI tools (like `awk`, `sort`, `sed`, etc.) to compute windowed aggregations and output the results in multiple formats.

The script must perform the following operations:
1. **Calculate Net Change**: For every event, compute the net change in bytes: `NET_BYTES = BYTES_ADDED - BYTES_REMOVED`.
2. **Sort the Data**: Order the events first by `CONFIG_KEY` (alphabetically), and then by `TIMESTAMP` (chronologically ascending).
3. **Windowed Rolling Average**: For each `CONFIG_KEY`, calculate a rolling average of the `NET_BYTES` over a window of the **last 3 changes** (the current change and up to 2 previous changes for that specific key). 
   * Use integer division (truncate towards zero, standard shell/awk behavior) for the average.
   * If a key has fewer than 3 events so far, average over the available events (e.g., divide by 1 for the first event, 2 for the second).
4. **CSV Output**: Write the processed stream to `/home/user/rolling_averages.csv` with the exact format:
   `TIMESTAMP,SERVER_ID,CONFIG_KEY,NET_BYTES,ROLLING_AVG`
   (Do not include a header row).
5. **JSON Aggregation**: Identify the single `CONFIG_KEY` that experienced the highest *absolute* rolling average at any point in its history. Write this result to `/home/user/max_volatility.json` in strictly this JSON format:
   `{"max_key": "<CONFIG_KEY>", "max_abs_avg": <INTEGER_VALUE>}`
   (If there is a tie, output the one that comes first alphabetically).

**Constraints & Details**:
- Do not use Python, Perl, or Ruby. You must use Bash and standard Unix text processing utilities (e.g., `awk`, `sort`, `grep`, `head`, `tail`).
- You can assume the input file has no malformed lines.
- Ensure your script `/home/user/process_configs.sh` is executable and run it to produce the output files.