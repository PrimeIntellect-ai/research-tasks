You are tasked with writing a Python script that acts as a mock "Kubernetes operator" to manage routing manifests and simulate firewall/load-balancer configurations on the filesystem.

In `/home/user/manifests/`, there are several JSON files representing desired state configurations for an internal reverse proxy. However, some of these files may be malformed, corrupted, or missing required fields. 

You must create a robust Python script at `/home/user/operator.py` that performs the following tasks:

1. **Read and Validate Manifests**:
   - Iterate through all `.json` files in `/home/user/manifests/`.
   - A valid manifest must be valid JSON and contain exactly these three keys: `route` (string), `target_port` (integer), and `allowed_ips` (list of strings).
   - If a file is not valid JSON, write the exact line `ERROR: Invalid JSON in <filename>` to `/home/user/operator.log`.
   - If a file is valid JSON but missing keys or has incorrect types, write the exact line `ERROR: Invalid schema in <filename>` to `/home/user/operator.log`.

2. **Idempotent Configuration Generation**:
   - Combine all valid manifests into a single consolidated reverse proxy configuration file at `/home/user/proxy_config.json`.
   - The format of `/home/user/proxy_config.json` must be a JSON object where the keys are the `route` strings, and the values are objects containing `target_port` and `allowed_ips`.
   - If multiple valid files define the *same* `route`, the file with the lexicographically latest filename (e.g., `z_route.json` overrides `a_route.json`) should take precedence.

3. **Logging Requirements**:
   - Start the log `/home/user/operator.log` with the line `OPERATOR RUN STARTED`.
   - After processing all files, for every route successfully added to the final configuration, write a line: `SUCCESS: Configured route <route> to port <target_port>` in alphabetical order of the routes.
   - End the log with `OPERATOR RUN COMPLETED`.

Your script must be robust, properly handling file I/O errors and schema validation without crashing. Do not hardcode the names of the files in the directory. Run your script once before completing the task to generate the required outputs.