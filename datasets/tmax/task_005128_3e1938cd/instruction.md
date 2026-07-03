You are a container specialist managing a microservice architecture. Our microservices dynamically request local filesystem mounts and storage quotas via JSON configuration files. We need to build an automated sanitization pipeline to ensure these requests are valid and secure before they are applied to the host filesystem.

Part 1: Fix the Vendored Package
We use a custom library called `fsmeta-utils` to handle some of the filesystem metadata and quota validation. The source code is pre-vendored at `/app/vendored/fsmeta-utils`. However, the previous maintainer left a bug in the code, and the package currently fails to install or run. 
1. Identify and fix the deliberate perturbation in `/app/vendored/fsmeta-utils/fsmeta/validators.py`.
2. Install the package in your user environment (`pip install --user -e /app/vendored/fsmeta-utils`).

Part 2: Locale and Timezone Configuration
Ensure your user environment's default timezone operations (via the `TZ` environment variable) are set to `Etc/UTC` to avoid timezone parsing anomalies during the validation step.

Part 3: The Sanitizer Script
Write a Python script at `/home/user/validate_mounts.py`. The script should be executable and take exactly one argument: the path to a directory containing JSON configuration files.

Each JSON file looks like this:
```json
{
  "service_id": "analytics-worker",
  "mount_path": "/data/analytics",
  "quota_bytes": 53687091200,
  "log_timezone": "America/New_York"
}
```

Your script must read all `.json` files in the provided input directory and apply the following validation rules:
1. **Path Traversal Prevention**: The `mount_path` must be strictly a subdirectory of `/data/` after resolving all `.` and `..` components. For example, `/data/service` is valid, but `/data/../etc` or `/var/lib/data` are invalid.
2. **Quota Limits**: The `quota_bytes` must be a positive integer and must not exceed 100 GB (100 * 1024 * 1024 * 1024 bytes).
3. **Locale/Timezone Validity**: The `log_timezone` must be a valid IANA timezone string (you can use standard Python libraries like `zoneinfo` or `pytz` to validate this).

If a file passes all rules, your script must copy the exact JSON file to the directory `/home/user/accepted_mounts/` (creating the directory if it doesn't exist).
If a file violates ANY rule, your script must NOT copy it. Instead, it must append the base filename (e.g., `req_12.json`) to a log file located at `/home/user/rejected.log`, with one filename per line.

Ensure your script is robust and correctly handles the directory input. An automated verifier will call `/home/user/validate_mounts.py <test_directory>` containing both clean and adversarial files.