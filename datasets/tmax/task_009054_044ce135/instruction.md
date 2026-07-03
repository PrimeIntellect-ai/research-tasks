You are tasked with writing a complex Bash utility that simulates an intelligent API Gateway log processor. In modern microservice architectures, requests often need to be dynamically routed based on semantic versioning, while enforcing strict validation and rate limiting.

Your goal is to write a Bash script at `/home/user/router.sh` that parses a server log file, evaluates each request against a JSON configuration of available backend services, and outputs a structured JSON file of the successfully routed requests.

**Inputs:**
1. **Server Log File (`/home/user/requests.log`):**
   Contains incoming HTTP requests, one per line, space-separated:
   `<timestamp> <ip_address> <http_method> <request_path>`
   Example: `1700000000 192.168.1.1 GET /api/auth/v1.2.5`

2. **Routes Configuration (`/home/user/routes.json`):**
   A JSON array of available backend services.
   ```json
   [
     {"service": "auth", "version": "1.0.0", "port": 8080},
     {"service": "auth", "version": "1.2.0", "port": 8081},
     {"service": "auth", "version": "2.0.0", "port": 8083}
   ]
   ```

**Processing Rules:**
Your script `/home/user/router.sh` must process the log file line by line and apply the following rules in order. If a request violates any rule, it must be completely dropped.

1. **Request Validation & URL Parsing:**
   - The HTTP method MUST be `GET`.
   - The request path MUST match the exact format: `/api/<service_name>/v<MAJOR>.<MINOR>.<PATCH>` (e.g., `/api/auth/v1.2.5`).

2. **Rate Limiting:**
   - Implement a strict IP-based rate limit: A maximum of 2 requests per IP address are allowed within any rolling 5-second window.
   - Example: If requests from an IP come at `T=1`, `T=3`, and `T=5`, the third request at `T=5` is dropped because the window `[1, 5]` already has 2 allowed requests (at `T=1` and `T=3`). A request at `T=7` would be allowed.

3. **Semantic Version Routing:**
   - Extract the requested `<service_name>` and `<MAJOR>.<MINOR>.<PATCH>`.
   - Look up the available versions for that service in `routes.json`.
   - **Resolution Rule:** Route to the highest available version of the service that has the *same MAJOR version* as the requested version, and is *less than or equal to* the requested MINOR and PATCH versions. 
   - If no available backend version satisfies this requirement, drop the request.

**Output:**
For all requests that successfully pass validation, rate limiting, and version routing, output a single JSON array to `/home/user/routed.json` containing objects with the following keys:
`timestamp` (integer), `ip` (string), `service` (string), `requested_version` (string, e.g., "1.2.5"), `routed_port` (integer).

**Execution:**
Your script must be executable and accept two arguments: the log file and the routes file.
`./router.sh /home/user/requests.log /home/user/routes.json`

Do not use external scripting languages like Python or Perl to bypass the bash constraints; however, standard tools like `jq`, `awk`, `sed`, `grep`, and `sort` are fully allowed and expected.