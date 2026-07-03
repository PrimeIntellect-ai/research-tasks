You are tasked with fixing and completing a local data ingestion pipeline. We have a multi-service setup that receives CSV files containing mathematical experiment tracking data, aggregates them, and stores the results. Recently, a silent data type corruption issue (similar to pandas silently converting integers to floats when NaNs are introduced) has been polluting our downstream dimensionality reduction models.

Your objective is twofold:
1. **Fix the multi-service pipeline:** We have an Nginx reverse proxy, a Flask API, and a Redis instance located in `/home/user/app/`. When you run `/home/user/app/start_services.sh`, they will start. However, the end-to-end flow is currently broken. Nginx is supposed to listen on port 8080 and route requests for `/api/` to the Flask app running on port 5000. You need to modify the Nginx configuration file located at `/home/user/app/nginx/nginx.conf` so that any POST request to `http://localhost:8080/api/upload` successfully reaches the Flask app. 

2. **Create a Data Sanitizer:** Write a Bash script at `/home/user/sanitizer.sh`. This script will act as a strict tabular data filter. 
   - It must take a single argument: the path to a CSV file.
   - It must analyze the 4th column (named `experiment_id`) of the CSV.
   - If *every* value in the 4th column (skipping the header) is a valid, strict integer (e.g., `12`, `-3`), the script should exit with code `0` (Accept).
   - If *any* value in the 4th column is empty, a float (e.g., `12.0`), `NaN`, `null`, or any other string, the script should exit with code `1` (Reject).
   - The script must rely entirely on Bash primitives or standard Unix tools (like `awk`, `sed`, `grep`). Do not use Python or R.

Once your `sanitizer.sh` is written and the Nginx proxy is correctly routed, you must verify your script against the test corpora located in `/home/user/data/clean/` and `/home/user/data/evil/`. 

Output your final verification logs to `/home/user/verification.log` with the format:
`[filename]: [ACCEPT/REJECT]` for every file in both the clean and evil directories.