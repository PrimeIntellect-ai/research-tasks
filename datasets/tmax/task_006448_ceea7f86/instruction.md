You are tasked with fixing and upgrading a configuration management audit pipeline. 

Currently, a scheduled pipeline processes a CSV audit log of server configuration changes. However, it uses a naive text processing tool that silently breaks and drops records when the configuration `Value` contains embedded newlines (which is common for full configuration file backups).

Your goal is to build a robust data processing script that correctly parses the CSV, handles embedded newlines, extracts specific metrics, and computes a rolling aggregate.

**Input Data:**
You have a CSV file located at `/home/user/audit_log.csv` with the following columns:
`Timestamp,Server,Key,Value`
*Note: The `Value` column is enclosed in double-quotes (`"`) and frequently contains embedded newline characters.*

**Processing Requirements:**
1. **Filter:** Keep only the records where `Key` is exactly `nginx_config`.
2. **Transform (Summary Statistic):** For the `Value` field, calculate the total number of lines it contains. (e.g., a string with no newlines is 1 line; a string with one embedded newline is 2 lines).
3. **Aggregate (Windowed/Rolling):** For each `Server`, calculate a 2-event Simple Moving Average (SMA) of the line count, ordered chronologically by `Timestamp`. 
   - The window size is 2 (the current event and the immediately preceding event for that specific server).
   - For the first event of a server, the moving average is simply the line count of that event.

**Output Specification:**
Write the results to a new CSV file at `/home/user/rolling_stats.csv`.
- The file must contain a header: `Server,Timestamp,LineCount,MovingAvg`
- Sort the output primarily by `Server` (alphabetical) and secondarily by `Timestamp` (ascending numerical).
- The `MovingAvg` should be formatted to exactly one decimal place (e.g., `4.0`, `5.5`).

You may use Bash, AWK, Python, or any other standard tools available in a standard Linux environment.