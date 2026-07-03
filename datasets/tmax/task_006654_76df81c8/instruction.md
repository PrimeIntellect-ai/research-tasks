You are a DevOps engineer investigating a compromised and failing application environment. You have been provided with artifacts from a container that recently crashed. Your goal is to perform a forensic analysis using standard Bash CLI tools to identify the root cause of the crash, a related build failure, and a suspicious embedded secret.

You must complete three distinct forensic objectives. 

**Objective 1: Statistical Anomaly Detection**
There is a web access log located at `/home/user/access.log`. The application crashed because a single IP address sent an anomalous burst of requests within a specific 1-minute window.
- Analyze the log to find the IP address that made exactly 1,337 requests in any single 1-minute window (format of timestamp in log: `[DD/MMM/YYYY:HH:MM:SS +0000]`).
- Write only the anomalous IP address to `/home/user/anomaly_ip.txt`.

**Objective 2: Linker Error Interpretation**
The CI/CD pipeline failed to rebuild the application container after the crash. The massive build log is located at `/home/user/build.log`.
- Find the specific missing C function symbol that caused the `ld` (linker) step to fail with an "undefined reference" error.
- Write only the exact name of the missing function symbol (e.g., `my_missing_function`) to `/home/user/missing_symbol.txt`.

**Objective 3: Binary Reverse Engineering**
A suspicious, un-stripped legacy binary was found in the container at `/home/user/legacy_parser`. We suspect it contains a hardcoded debug password.
- Extract the strings from this binary. Look for a string that starts with `DEBUG_PWD=`.
- Write only the value of the password (the part *after* the equals sign) to `/home/user/binary_secret.txt`.

You are expected to use standard Bash utilities (e.g., `awk`, `grep`, `sort`, `uniq`, `strings`) to complete this task. Do not use external scripting languages like Python or Ruby.

Ensure all three output files are created with exactly the required content, no trailing spaces or extra text, just the raw requested value.