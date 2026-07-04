You are a system administrator tasked with fixing our internal log ingestion pipeline. The pipeline involves a Python utility that parses localized timestamps, and an Nginx reverse proxy that routes traffic to a backend UNIX socket. 

There are three parts to this task:

1. **Fix the Vendored Package:**
   We use a vendored version of `dateparser` located at `/app/vendor/dateparser`. However, someone made a bad edit to the source code, and trying to import it currently throws an error. Identify the perturbation in the vendored source and fix it so the package can be successfully installed and imported in the local user environment.

2. **Idempotent Nginx Configuration:**
   Write a Python script at `/home/user/setup_proxy.py` that performs idempotent setup of an unprivileged Nginx instance. 
   - It must generate an Nginx configuration file at `/home/user/nginx/nginx.conf`.
   - The Nginx server must listen on port 8080.
   - All requests to `/` must be reverse-proxied to a UNIX socket located exactly at `/tmp/backend_app.sock`.
   - The script must start the Nginx process in the background using this configuration. If Nginx is already running with the correct configuration, the script should do nothing. If the configuration is missing or Nginx is not running, it should set it up and start it.

3. **Log Timestamp Converter (Fuzz Equivalence):**
   Write a robust Python script at `/home/user/log_converter.py`. This script will be called with two command-line arguments: an ISO-8601 timestamp string (with varying offsets) and a target locale (e.g., `fr_FR`, `de_DE`).
   - The script must parse the timestamp using the fixed `dateparser` package.
   - It must convert the parsed time to the `UTC` timezone.
   - It must output the formatted date and time to `stdout` in exactly the format produced by our reference oracle located at `/app/oracle/log_converter_oracle`. 
   - We will test your script by fuzzing it with thousands of random timestamps and locales to ensure bit-exact equivalence with the oracle. Ensure your script gracefully handles invalid dates by printing "INVALID_DATE" and exiting with code 1.