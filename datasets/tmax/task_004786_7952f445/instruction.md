You are an integration developer responsible for testing a new backend API by migrating some legacy data. You need to configure a local reverse proxy, write a data processing script in Bash to handle a schema migration, and send the migrated data through the proxy.

Your environment has a Python mock server running on port 9000 that simulates the new backend API. Nginx is installed on the system.

Please complete the following tasks:

1. **Reverse Proxy Configuration:**
   Create an Nginx configuration file at `/home/user/nginx.conf`. It must:
   - Run as the current user (do not use port 80 or root privileges).
   - Listen on `127.0.0.1:8080`.
   - Route all requests starting with the path `/v2/` to the mock API running at `http://127.0.0.1:9000/` (make sure to strip the `/v2/` prefix when proxying to the backend, or just proxy to the root if the backend expects the relative paths without `/v2`. The mock server expects the endpoint `/import`). So a request to `http://127.0.0.1:8080/v2/import` should proxy to `http://127.0.0.1:9000/import`.
   - Set the necessary temp paths (e.g., `client_body_temp_path`, `proxy_temp_path`, `pid`, etc.) to directories inside `/home/user/` so Nginx can start without root access.
   - Start the Nginx server using this configuration.

2. **Schema Migration:**
   You have a legacy CSV file at `/home/user/legacy_data.csv` with the following header:
   `id,full_name,role`

   Write a Bash script at `/home/user/migrate.sh` that reads this CSV file (skipping the header) and transforms each row into a new JSON schema:
   - `identifier`: integer (mapped from `id`)
   - `display_name`: string (mapped from `full_name`)
   - `is_admin`: boolean (`true` if `role` is exactly `"admin"`, otherwise `false`)

   Example JSON payload:
   `{"identifier": 101, "display_name": "Alice Smith", "is_admin": true}`

3. **Data Processing and API Testing:**
   Your `/home/user/migrate.sh` script must send a `POST` request with the JSON payload for each row to the reverse proxy at `http://127.0.0.1:8080/v2/import`.
   - Ensure the `Content-Type: application/json` header is set.
   - For each request, capture the HTTP status code returned by the server.
   - Append the result of each row's migration to `/home/user/migration_results.log` in the format: `ID <id>: HTTP <status_code>`.

Run your Bash script to perform the migration. You are finished when `/home/user/migration_results.log` contains the status codes for all rows in the CSV.