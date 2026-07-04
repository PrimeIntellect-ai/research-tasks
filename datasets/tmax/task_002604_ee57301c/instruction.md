You are a data analyst tasked with setting up a robust data ingestion pipeline for financial transaction CSV files. You need to write a Bash-based data sanitiser and configure the multi-service architecture to use it.

First, write a Bash script at `/home/user/filter.sh` that reads CSV rows from standard input (stdin) and writes valid rows to standard output (stdout). 
A row is considered valid (clean) ONLY if it meets all of the following criteria:
1. It has exactly 4 columns separated by commas.
2. Column 1 (TransactionID) contains only numeric digits.
3. Column 2 (UserID) contains only numeric digits.
4. Column 3 (Amount) is a strictly positive number (e.g., `10.50`, `3`, `0.01` but not `0`, `-5.2`, or `abc`).
5. Column 4 (Description) contains only alphanumeric characters and spaces.
If a row is invalid (evil/malformed), it must be silently dropped. The script should process data line-by-line indefinitely. Make sure to `chmod +x` your script.

Second, integrate this script into our ingestion services located in `/home/user/app/`. The system consists of:
- Nginx (acting as the entrypoint on port 8080)
- A Python Flask Ingestion API
- A Redis cache (running on port 6379)

You must fix the configurations to establish the following end-to-end flow:
1. Nginx must proxy requests from `http://localhost:8080/upload` to the Flask API. Modify `/home/user/app/nginx.conf` so that the `/upload` location proxies to `http://127.0.0.1:5000`.
2. The Flask API needs to know where Redis is and what filter script to use. Edit `/home/user/app/settings.env` and set:
   - `REDIS_PORT=6379`
   - `FILTER_SCRIPT=/home/user/filter.sh`

Once you have written the script and fixed the configurations, start the services by running the provided script `/home/user/app/start_services.sh` (you don't need to write this, it already exists).