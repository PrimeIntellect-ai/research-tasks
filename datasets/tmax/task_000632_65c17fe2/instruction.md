You are a data analyst managing an employee directory pipeline. We have a multi-service setup that processes CSV uploads containing employee hierarchies.

The pipeline consists of:
1. An Nginx reverse proxy listening on port 8080.
2. A Python Flask application listening on port 5000 that handles the CSV processing.

Currently, the pipeline is broken and lacks validation. Your task is to fix the pipeline configuration and implement a robust validation script in Bash.

Step 1: Fix the Services
The services are located in `/app/`. The Nginx configuration is at `/app/nginx.conf` and the Flask app is at `/app/app.py`.
- Configure `/app/nginx.conf` to correctly proxy requests for `/upload` to the Flask app on `127.0.0.1:5000`.
- The Flask app expects a validation script to exist at `/home/user/validate.sh`.
- Start the services (you can run Nginx with `nginx -c /app/nginx.conf` and Flask with `python3 /app/app.py &`).

Step 2: Create the Validation Script
Create a Bash script at `/home/user/validate.sh` that takes a single argument: the path to a CSV file.
The CSV files have three columns without a header: `id`, `name`, `manager_id`. (e.g., `1,Alice,`, `2,Bob,1`).
The script must:
- Return exit code 0 if the CSV is valid.
- Return exit code 1 if the CSV is invalid.

A CSV is considered "invalid" (evil) if it contains a circular management chain (e.g., Employee A manages Employee B, and Employee B manages Employee A, directly or indirectly). 
To do this efficiently, your script should use `sqlite3` to load the CSV into an in-memory database, create an appropriate index on `manager_id` for query optimization, and run a recursive CTE (Common Table Expression) to detect cycles.

The system will verify your solution by POSTing files to `http://localhost:8080/upload`. Ensure your script works perfectly, as it will be tested against a hidden corpus of clean and evil (cyclic) CSV files.