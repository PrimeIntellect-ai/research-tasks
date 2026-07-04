You are a monitoring specialist tasked with setting up an automated alerting system for a legacy application. This application only provides its health status via an interactive command-line interface, which requires user input to proceed.

Your objective is to build an automated, idempotent monitoring wrapper using Bash and Expect.

**Environment Details:**
* The legacy CLI tool is located at `/home/user/legacy_app/cli_tool.sh`. 
* When executed, it interactively prompts: `Please enter diagnostic PIN:`
* The PIN you must use is `8472`.
* After receiving the correct PIN, it outputs several lines of telemetry, but you only care about the line starting with `[STATE] ` (e.g., `[STATE] CRITICAL_ERROR` or `[STATE] HEALTHY`).

**Your Tasks:**

1. **Write an Expect Script (`/home/user/scripts/check_health.exp`)**
   * Write an `expect` script that automates the interaction with `/home/user/legacy_app/cli_tool.sh`.
   * It must supply the PIN `8472` when prompted.
   * It must capture the output and print *only* the line that begins with `[STATE] ` to standard output.

2. **Write a Bash Wrapper Script (`/home/user/scripts/alert_manager.sh`)**
   * This script will act as a cron-like executable to manage the alert lifecycle. It must be completely idempotent.
   * **Directory Management:** When run, it must ensure the following directories exist:
     * `/home/user/alerts/active`
     * `/home/user/alerts/resolved`
   * **Execution:** It must execute your `check_health.exp` script to get the current state.
   * **Failure Handling (if state is `[STATE] CRITICAL_ERROR`):**
     * Check if a symlink exists at `/home/user/alerts/active/current_alert.link`.
     * If the symlink *does not exist*, create a new log file in `/home/user/alerts/active/` named `incident_<timestamp>.log` (using `date +%s` for the timestamp). Write the exact state string (e.g., `[STATE] CRITICAL_ERROR`) into this file. Then, create a symlink at `/home/user/alerts/active/current_alert.link` pointing to this new log file.
     * If the symlink *already exists*, do absolutely nothing (an alert is already active and unacknowledged).
   * **Recovery Handling (if state is `[STATE] HEALTHY`):**
     * Check if `/home/user/alerts/active/current_alert.link` exists.
     * If it exists, move the file that the symlink points to into `/home/user/alerts/resolved/` (keep its original `incident_<timestamp>.log` filename). Then, delete the symlink `/home/user/alerts/active/current_alert.link`.
     * If the symlink does not exist, do absolutely nothing.

Ensure both of your scripts are executable (`chmod +x`). You can test your scripts by running `/home/user/scripts/alert_manager.sh`. The legacy application's output will change depending on the contents of `/home/user/legacy_app/internal_state.dat`, which you can modify manually to test your script's behavior in both healthy and error scenarios.