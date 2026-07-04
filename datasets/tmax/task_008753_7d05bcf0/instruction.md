You are a configuration manager tasked with tracking the evolution of server configurations over time to identify configuration drift.

We have an SQLite database located at `/home/user/configs.db`. It contains a table named `server_configs` with the following schema:
`CREATE TABLE server_configs (id INTEGER PRIMARY KEY, hostname TEXT, config_text TEXT);`

Each row represents a snapshot of a server's configuration. However, many configurations are functionally identical, differing only by comments or whitespace. 

Your task is to write a script (using Bash, Python, or standard Linux tools) that does the following:
1. Extracts all records from the `server_configs` table.
2. Normalizes the `config_text` for each record using the following rules, strictly in this order:
   - Split the text into lines.
   - Strip all leading and trailing whitespace (spaces and tabs) from each line.
   - Completely discard any line that is empty (0 length) after stripping.
   - Completely discard any line that starts with a `#` character.
   - Recombine the remaining lines using a single newline (`\n`) character. Do not add a trailing newline to the final string unless there is only one line.
3. Computes the SHA-256 hash of the resulting normalized configuration string.
4. Groups the records by `hostname` and counts the number of **unique** normalized configurations (hashes) each server has had.
5. Outputs a CSV report to `/home/user/report.csv` with the exact header `hostname,unique_configs`.
6. Sorts the output descending by the `unique_configs` count, and then ascending by `hostname` for ties.

Make sure your final output is exactly formatted as requested and placed at `/home/user/report.csv`.