You are tasked with analyzing a system's configuration change log to identify "flapping" configurations. A configuration is flapping if it repeatedly toggles back and forth between states, which is a strong indicator of an automated system conflict or a struggling configuration manager.

You have been provided a chronological log of configuration updates at `/home/user/config_updates.csv`.
The CSV has no header and uses the format: `Timestamp,Environment,Key,Value`

**Definitions:**
*   **Update Sequence:** For any given `(Environment, Key)` pair, its updates occur in chronological order (the order they appear in the file).
*   **Flap:** A "flap" occurs when a configuration key's `Value` is updated, and its new value is exactly the same as the value it had *two updates ago*, but different from the *immediately preceding* value. 
    *   *(i.e., For a sequence of values $V$ for a specific Environment and Key, a flap occurs at index $i \ge 3$ if $V_i == V_{i-2}$ AND $V_i \neq V_{i-1}$).*

**Your Objective:**
1. Build a multi-stage data processing pipeline to detect every flap in the log.
2. Calculate the total number of flaps for every `(Environment, Key)` pair.
3. Perform a stratified sampling operation: For *each* unique `Environment`, extract exactly one `Key` that has the highest total number of flaps.
    *   *Tie-breaker:* If multiple Keys in the same Environment tie for the highest flap count, select the one that comes first alphabetically.
4. Output your final report to `/home/user/flapping_report.csv`.

**Output Requirements:**
*   The output file `/home/user/flapping_report.csv` must contain a header row: `Env,Key,Flaps`
*   The rows must be sorted alphabetically by `Env`.
*   The format should be strict CSV.

*Example Output:*
```csv
Env,Key,Flaps
DEV,feature_flag_x,5
PROD,db_timeout,3
STAGING,worker_nodes,8
```