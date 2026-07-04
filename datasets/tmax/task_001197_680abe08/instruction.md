You are tasked with building a robust data processing pipeline for an analytics team. The team has been struggling with a legacy script that silently drops CSV rows containing embedded newlines, leading to inaccurate aggregate metrics. Your goal is to build a reliable Go-based web service that integrates with an existing multi-service setup.

Environment overview:
- An FTP server is running on `localhost:2121`. It contains several CSV files in the `/data/` directory. Credentials: username `ftpuser`, password `ftppass`.
- Nginx is installed but needs to be configured and started.

Your objectives:
1. **Pipeline Scheduling**: Create a shell script `/home/user/sync.sh` that uses `curl` or `lftp` to download all `.csv` files from `ftp://localhost:2121/data/` into `/home/user/local_data/`. Set up a user cron job to run this script every minute.
2. **Data Processing Service**: Write a Go web service (source in `/home/user/server.go`, compile and run it in the background) that listens on `127.0.0.1:9090`. 
   - It must expose a `GET /metrics` endpoint.
   - When accessed, the endpoint should read all CSV files currently in `/home/user/local_data/`.
   - The CSV files have headers: `TransactionID`, `Category`, `Amount`, `Notes`. 
   - Note: The `Notes` column often contains multi-language Unicode text and *embedded newlines*. You must parse the CSV correctly without dropping these rows.
   - The service should aggregate the sum of `Amount` (integer) grouped by `Category` (Unicode string).
   - Sort the grouped results descending by total `Amount`, and then alphabetically by `Category` for ties.
   - Return the result as a JSON array of objects: `[{"category": "Retail", "total": 5000}, ...]`.
3. **Integration**: Configure Nginx using a custom configuration file at `/home/user/nginx.conf`. It should run as the current user, listen on port `8080`, and act as a reverse proxy forwarding requests from `/api/metrics` to your Go service at `http://127.0.0.1:9090/metrics`. Start Nginx using this config.

Ensure your Go service is robust and handles CSV parsing natively with standard libraries to correctly process the embedded newlines. Leave your Go service and Nginx running.