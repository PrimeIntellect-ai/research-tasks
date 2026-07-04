You are a container specialist tasked with fixing and deploying a local microservice for our development environment. 

A previous engineer left behind a broken setup. Your goal is to extract the correct configuration, fix the system configuration files, and write a robust Python script to act as the API gateway.

Here are your instructions:

**Phase 1: Configuration Extraction**
There is a network log file located at `/home/user/logs/network_trace.log`. Use text processing pipelines (e.g., `grep`, `awk`, `sed`) to extract the internal authentication service endpoint.
1. Find the line containing `[CRITICAL] AUTH_BINDING_ESTABLISHED`.
2. Extract the IP address and port (format `IP:PORT`) from that line.
3. Save ONLY the extracted `IP:PORT` string to a new file at `/home/user/config/auth_endpoint.txt`.

**Phase 2: Microservice Dependency Configuration**
Our custom local service manager reads from `/home/user/config/services.json`. Currently, the `api-gateway` service fails to start because it tries to boot before the `auth-service`.
1. Modify `/home/user/config/services.json`.
2. Locate the `"api-gateway"` entry. Add `"auth-service"` to its `"depends_on"` array. 

**Phase 3: Gateway Script Implementation**
Write a robust Python script at `/home/user/api_gateway.py` that performs the following actions:
1. Reads the `IP:PORT` from `/home/user/config/auth_endpoint.txt`.
2. Configures the environment's Locale and Timezone for the gateway. Specifically, force the program's locale to `de_DE.UTF-8` (for time formatting) and the timezone to `Europe/Berlin`. 
3. Takes a specific Unix timestamp: `1716388800` (which is May 22, 2024, 12:00:00 UTC).
4. Converts this timestamp into a localized, timezone-aware string representation using the exact format: `%A, %d. %B %Y %H:%M:%S` (e.g., "Mittwoch, 22. Mai 2024 14:00:00"). Ensure the standard library `locale` and `zoneinfo` or `pytz` are used appropriately.
5. Writes a final log entry to `/home/user/logs/gateway_startup.log` with the exact text:
   `Gateway ready. Auth upstream: <IP:PORT>. Local startup time: <LOCALIZED_TIME_STRING>`
   (Replace `<IP:PORT>` and `<LOCALIZED_TIME_STRING>` with your actual calculated values).

*Note: Ensure your Python script handles file reading safely and cleanly. You may run your script to generate the final log file.*