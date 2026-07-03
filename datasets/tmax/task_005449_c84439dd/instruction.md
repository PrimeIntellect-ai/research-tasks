You are acting as a support engineer tasked with writing a diagnostic tool. We recently experienced a critical application crash, and we need to collect forensic data automatically. 

Our application consists of two main services (Frontend and Backend) that log in different formats. We suspect the crash was caused by a dependency conflict introduced during a recent system patch.

Please create a Bash script located at `/home/user/collect_diagnostics.sh` that performs the following forensic tasks when executed:

1. **Dependency Conflict Resolution**:
   - Read the expected requirements from `/home/user/system_state/app_requirements.txt`.
   - Read the currently installed system packages from `/home/user/system_state/packages.txt`.
   - Identify the exact package that is installed but whose version does NOT match the required version. (Assume there is exactly one such package).

2. **Log Timeline Reconstruction**:
   - The frontend logs are at `/home/user/logs/frontend.log` and use ISO 8601 timestamps (e.g., `2023-10-25T10:00:00Z`).
   - The backend logs are at `/home/user/logs/backend.log` and use UNIX epoch timestamps (e.g., `1698228001`).
   - Convert the backend UNIX timestamps to ISO 8601 format (in UTC, ending with 'Z', matching the frontend format exactly).
   - Merge both logs into a single chronological timeline.
   - Scan the merged, chronologically sorted timeline to find the exact timestamp of the very first line containing the string `[FATAL]`.

3. **Output Generation**:
   The script must write a summary report to `/home/user/diagnostics_report.txt` in exactly the following `KEY=VALUE` format:
   ```
   CONFLICTING_PACKAGE=<package_name>
   REQUIRED_VERSION=<version_from_requirements>
   INSTALLED_VERSION=<version_from_packages>
   FIRST_FATAL_TIMESTAMP=<ISO_8601_timestamp>
   ```

Make sure your script is executable (`chmod +x`). All time parsing should assume UTC. You may use standard Linux utilities (like `awk`, `date`, `grep`, `sort`, `join`) within your bash script.