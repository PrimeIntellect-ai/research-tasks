You are a Configuration Manager responsible for tracking configuration drift across thousands of servers. Your system periodically dumps the active configuration of all servers into a large, continually appended log file. 

Your task is to analyze this log file to extract mathematical metrics about the configurations, using only standard Bash tools (e.g., `awk`, `grep`, `sed`, `sort`, `uniq`, etc. No Python or Perl).

The configuration dump is located at: `/home/user/config_changes.csv`

The file is a pipe-delimited CSV (`|`) with the following columns:
1. `Timestamp` (YYYY-MM-DD HH:MM:SS)
2. `ServerID` (e.g., srv-001)
3. `Role` (e.g., web_server, db_node, cache)
4. `ConfigData` (A single string containing multiple key-value pairs)

The `ConfigData` string is formatted as pairs separated by semicolons (`;`), with keys and values separated by colons (`:`). 
Example `ConfigData`: ` Timeout: 30 ; max_connections :150; SSL:true `

Notice that spacing and capitalization are inconsistent.

**Your objectives:**
1. **Stream and Filter:** Process `/home/user/config_changes.csv` and isolate records where the `Role` is exactly `web_server` (ignore surrounding whitespace in the CSV columns if any).
2. **Tokenization and Normalization:** For the `web_server` records, extract the numeric value associated with the key `max_connections`. The key may appear in any case (e.g., `Max_Connections`, `MAX_CONNECTIONS`) and may have varying amounts of surrounding whitespace before the colon, after the colon, or around the semicolons.
3. **Sorting and Grouping:** Determine the frequencies of each unique `max_connections` value among the `web_server`s.
4. **Output 1:** Write the top 3 most frequent `max_connections` values and their exact counts to `/home/user/top_configs.txt`. Format each line exactly as `COUNT VALUE` (e.g., `250 100`), sorted in descending order of frequency. If there is a tie in count, sort by the value descending.
5. **Output 2 (Mathematical Aggregation):** Calculate the total mathematical sum of all extracted `max_connections` values for the `web_server` role. Write this single numeric sum to `/home/user/config_sum.txt`.

Ensure your solution relies entirely on standard Linux shell utilities.