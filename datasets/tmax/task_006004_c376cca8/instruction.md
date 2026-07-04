You are an infrastructure engineer automating the provisioning of a localized edge service. Because you are working in an environment without root privileges or full container runtime access, you need to manage the service lifecycle using basic Bash process management.

You need to create two Bash scripts in `/home/user`: `provision.sh` and `check_health.sh`.

**Step 1: Write `/home/user/provision.sh`**
This script must perform the following actions when executed:
1. Parse the configuration file located at `/home/user/raw_settings.conf`. This file contains key-value pairs in the format `Key: Value` (ignoring comments starting with `#` and empty lines).
2. Extract the values for `Timezone` and `Locale`.
3. Generate an environment file at `/home/user/service.env` containing exactly two lines:
   `TZ=<extracted_timezone_value>`
   `LC_ALL=<extracted_locale_value>`
4. Source the newly created `/home/user/service.env` and export these variables.
5. Launch the executable `/home/user/mock_app.sh` in the background. Its standard output and standard error must be redirected to `/home/user/app.log`.
6. Save the Process ID (PID) of the background process into `/home/user/app.pid`.

**Step 2: Write `/home/user/check_health.sh`**
This script will be used by our monitoring system. When executed, it must:
1. Read the PID from `/home/user/app.pid`.
2. Check if the process with that PID is currently running.
3. Check if the very last line of `/home/user/app.log` contains the exact word "HEARTBEAT".
4. If BOTH conditions are met, print exactly the string `HEALTHY` to standard output.
5. If EITHER condition fails, print exactly the string `UNHEALTHY` to standard output.

**Requirements:**
- Both scripts you create must be executable (`chmod +x`).
- Do not modify `/home/user/raw_settings.conf` or `/home/user/mock_app.sh`.
- Ensure `/home/user/provision.sh` exits cleanly after starting the background process.