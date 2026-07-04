You are a Cloud Architect migrating a set of legacy services to a new cloud-native environment. You need to create an automated, idempotent configuration pipeline and verify network connectivity before deploying. 

All your work should be done in `/home/user`. You have access to Python 3 and bash.

### Background
The legacy application configuration is currently stored in INI format at `/home/user/legacy/app.conf`. 
It contains legacy internal endpoints that need to be remapped to their new cloud equivalents (which, for the purpose of this sandbox testing environment, are mapped to local high ports).

### Requirements

**Phase 1: Configuration Migration Script (`/home/user/migrate_config.py`)**
Write a Python script that reads `/home/user/legacy/app.conf` and idempotently generates a new JSON configuration file at `/home/user/cloud/config.json`.
The mapping rules are:
- `db.local` (port 3306) maps to `localhost` port `33060`
- `redis.local` (port 6379) maps to `localhost` port `63790`
- The script must add a new top-level JSON key `"cloud_region"` with the value `"us-east-1"`.
- The final JSON structure must look like this:
  ```json
  {
    "cloud_region": "us-east-1",
    "database": {
      "host": "localhost",
      "port": 33060,
      "user": "admin"
    },
    "cache": {
      "host": "localhost",
      "port": 63790
    }
  }
  ```
(Note: Do not hardcode the user "admin"; extract it from the INI file). Ensure the directory `/home/user/cloud/` is created if it does not exist. The script must be idempotent (running it multiple times should yield the exact same JSON file and state without throwing errors).

**Phase 2: Connectivity Diagnostics Script (`/home/user/check_endpoints.py`)**
Write a Python script that reads the newly generated `/home/user/cloud/config.json` and performs a TCP connection test to both the database and cache endpoints (host and port) specified in the JSON file. 
- It must attempt to establish a short-lived socket connection to each endpoint.
- If both connections succeed, the script should exit with status code `0`.
- If any connection fails or times out, the script should print an error and exit with status code `1`.

**Phase 3: CI/CD Pipeline Script (`/home/user/pipeline.sh`)**
Write a bash script that coordinates the entire process:
1. Executes `migrate_config.py`.
2. Validates that `/home/user/cloud/config.json` contains valid JSON.
3. Executes `check_endpoints.py`.
4. If all previous steps are successful, it must write the exact string `DEPLOYMENT_READY` to `/home/user/deploy_success.log`. If any step fails, the script should exit and not create/write the success log.

Ensure all scripts have executable permissions. 

To test your scripts, mock services will be running in the background on ports 33060 and 63790. You can run `./pipeline.sh` to trigger the whole workflow.