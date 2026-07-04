You are a data analyst working in an environment where Python is unavailable. You only have access to standard Bash tools (coreutils, awk, sed, etc.).

We have a vendored data processing toolkit located at `/app/bash-csv-toolkit-1.2/` that is supposed to filter CSV files. However, the toolkit has a bug and is currently failing to correctly apply minimum score constraints.

Your objective:
1. Inspect and fix the `filter_valid.sh` script in `/app/bash-csv-toolkit-1.2/`. The script is intended to read CSV files and output only the rows where `age` (column 3) >= 18 and `score` (column 4) >= the environment variable `MIN_SCORE`. Look for a typo in how the environment variable is passed to the underlying `awk` command.
2. In `/home/user/data/`, there are several CSV files (`part_1.csv` to `part_5.csv`). They all have the header `id,name,age,score`.
3. Set `MIN_SCORE=50` and use the fixed `filter_valid.sh` to process all 5 CSV files **in parallel**. 
4. Aggregate the results to find the total sum of the `score` column for all valid rows across all files. Save this single numeric sum to `/home/user/sum.txt`.
5. Finally, orchestrate a simple HTTP server using `nc` (netcat) listening on `127.0.0.1:8080`. Whenever it receives a request, it must respond with a valid HTTP 200 response (e.g., `HTTP/1.1 200 OK\r\n\r\n`) followed by the computed sum in the body. Ensure this server runs in the background and can handle multiple sequential requests (using a `while true` loop).

Complete this task entirely in Bash. Do not use Python, Perl, or any other scripting languages.