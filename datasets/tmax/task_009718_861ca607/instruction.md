You are tasked with building a Go-based configuration change tracker that processes configuration logs from a fleet of servers. The system receives logs in CSV format, but the configuration values often contain tricky formatting like embedded newlines. 

You need to write a Go program located at `/home/user/tracker/process.go` that reads `/home/user/raw_configs.csv` and outputs a processed dataset to `/home/user/processed_configs.csv`.

**Input Format (`/home/user/raw_configs.csv`):**
A CSV file with four columns: `Timestamp,Server,Key,Value`.
*Note: The `Value` column may contain quoted text with embedded newlines. Your parser must handle this correctly without silently dropping rows.*

**Processing Requirements:**
For each unique `Server` and `Key` combination, you must process the rows in chronological order (top to bottom) and apply the following logic:

1. **Hash-Based Deduplication:** 
   Compute the SHA256 hash of the `Value`. If the hash is identical to the *immediately preceding accepted* hash for that specific `Server` and `Key`, you must silently drop the row (it represents no actual config change).

2. **Distance Computation (Configuration Drift):**
   For accepted changes, calculate the Levenshtein distance between the *previous* accepted `Value` and the *current* `Value` for that `Server` and `Key`. If this is the first time a `Server` + `Key` is seen, the distance is `0`.

3. **Rolling Statistics:**
   Keep track of the byte length of the accepted `Value` strings. Calculate the rolling average of the length of the *last 3 accepted* values (or fewer, if less than 3 have been accepted so far) for that `Server` and `Key`.

**Output Format (`/home/user/processed_configs.csv`):**
Write the accepted changes as a CSV file with the following columns:
`Timestamp,Server,Key,ValueHash,Drift,RollingAvg`
- `ValueHash`: The SHA-256 hash of the `Value` as a lowercase hex string.
- `Drift`: The Levenshtein distance integer.
- `RollingAvg`: The rolling average of the byte length of the last up to 3 values, formatted exactly to 2 decimal places (e.g., `15.00`, `13.67`).

**Setup Instructions:**
1. You may initialize a Go module in `/home/user/tracker` and download third-party packages if you prefer not to implement Levenshtein distance from scratch.
2. Ensure your program compiles and runs successfully, writing exactly to `/home/user/processed_configs.csv`.