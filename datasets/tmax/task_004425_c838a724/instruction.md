You are acting as a data engineer assisting a security log analyst. We have a large batch of security logs in JSON-Lines format located at `/home/user/logs/raw_events.jsonl`. 

We are specifically investigating "login" events. However, the system that generated these logs encodes usernames using Unicode escape sequences (e.g., `\u0021` for `!`, `\u0061` for `a`), and standard command-line tools like `jq` are currently breaking or running too slowly on our legacy infrastructure when trying to parse the malformed lines scattered in the file.

Your task is to build a fast, parallel processing pipeline using C and Bash to extract and normalize this data.

Step 1: Write a C program
Create a C program at `/home/user/parser.c` that reads lines from standard input (stdin).
For each line:
- Check if the "event" field has the value "login". If not, skip the line.
- The JSON lines have a strict schema and no nested objects. They always look exactly like this:
  `{"timestamp":"2023-10-24T08:15:30Z","event":"login","user":"admin\u0021"}`
- Extract the `timestamp` and parse it from the ISO8601 format (`YYYY-MM-DDThh:mm:ssZ`) into a Unix epoch integer. You can assume UTC.
- Extract the `user` string and decode any `\uXXXX` escape sequences into their literal ASCII characters. (You only need to handle basic ASCII characters in the range `\u0020` to `\u007E`).
- Output the normalized data to standard output (stdout) in CSV format: `epoch_time,decoded_user`

Step 2: Build and Orchestrate
Compile your C program to `/home/user/parser`.
Write a Bash script at `/home/user/process.sh` that does the following:
1. Splits the `/home/user/logs/raw_events.jsonl` file into smaller chunks (e.g., 5 lines per chunk) inside a temporary directory `/home/user/tmp_chunks/`.
2. Uses `xargs` or a similar Bash construct to run your compiled `/home/user/parser` on all chunks in parallel (e.g., using 4 concurrent processes).
3. Collects all the CSV outputs, sorts them chronologically by `epoch_time` (ascending), and writes the final output to `/home/user/processed_logins.csv`.

Ensure your C code handles basic string searching efficiently and your bash script successfully orchestrates the parallel execution. Run your bash script to generate the final CSV.