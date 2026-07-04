You are acting as a log analyst setting up an ingestion pipeline for internationalized threat logs. We receive JSON-lines formatted logs from global sensors, but our current tools have a bug with Unicode escape sequences. 

Your task involves fixing a vendored script, setting up a Bash-based HTTP service to process incoming logs, and configuring a cron job for aggregation.

**Step 1: Fix the Vendored Package**
We have a vendored package located at `/app/bash-jaccard-logger-1.0`. This package contains a script `process_log.sh` that takes two string arguments, normalizes them (lowercasing, removing punctuation), and computes the Jaccard similarity coefficient (0.0 to 1.0) between their word sets. 
However, it has a deliberate perturbation: it fails to handle Unicode escape sequences (e.g., `\u00e9` for `é`). The script contains a broken attempt to parse these. You must patch `/app/bash-jaccard-logger-1.0/process_log.sh` so that it correctly decodes JSON Unicode escape sequences into actual UTF-8 characters *before* it calculates the similarity. 
*Hint:* You can use `jq -r` or bash `printf` to evaluate the unicode characters properly.

**Step 2: Create a Log Ingestion Service**
Using Bash and `socat` (or `nc`), create a script at `/home/user/server.sh` and run an HTTP server listening on `127.0.0.1:9090`. 
- The server must handle HTTP `POST` requests.
- It must reject requests that do not have the exact HTTP header: `Authorization: Bearer log-auth-key-881` (return HTTP 401 Unauthorized).
- The POST body will be a JSON-lines payload. Each line is a JSON object with two fields: `"message"` and `"baseline"`.
- For each line, extract the `"message"` and `"baseline"` fields, and run them through `/app/bash-jaccard-logger-1.0/process_log.sh`.
- Append the output score of each processed line to `/tmp/processed_logs.txt` (one score per line).
- The HTTP response body must be the list of similarity scores computed for that request (one per line), with a `200 OK` status.

**Step 3: Scheduled Aggregation**
Create an aggregation script at `/home/user/aggregate.sh` that calculates the arithmetic mean of all the scores in `/tmp/processed_logs.txt`. It should write this single float value (rounded to 2 decimal places) to `/tmp/average_sim.txt`.
Then, install a user cron job for the user `user` that executes `/home/user/aggregate.sh` every minute.

Leave the `socat` HTTP server running in the background when you are done. Ensure `/tmp/processed_logs.txt` is created and writable.