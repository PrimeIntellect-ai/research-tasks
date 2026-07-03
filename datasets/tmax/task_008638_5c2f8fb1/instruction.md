You are a security auditor investigating a compromised Linux server. You need to analyze authentication logs and suspicious binaries. However, because the binaries might be trapped or malicious, you must perform your analysis within a restricted sandbox.

Your objective is to write two Bash scripts. 

**Part 1: The Analysis Script**
Create a Bash script at `/home/user/audit_script.sh` that takes exactly two arguments:
1. The path to an SSH authentication log file.
2. The path to a directory containing binaries.

The script must perform the following tasks:
A. **Authentication Flow Analysis:** Parse the provided auth log file to find any IP address that successfully logged in (indicated by "Accepted password") *after* having at least 3 "Failed password" attempts for the exact same username. Write the sorted, unique list of these breached IP addresses (one per line) to `/home/user/breached_ips.txt`.
B. **Binary & Permission Analysis:** Scan the provided directory for ELF binaries. Identify any binary that meets **both** of the following criteria:
   - The file has the SUID (Set owner User ID) permission bit set.
   - The binary has an RPATH or RUNPATH that exactly matches `/tmp` (which can be determined using `readelf -d`).
Write the basenames of these vulnerable binaries (one per line) to `/home/user/vulnerable_binaries.txt`.

**Part 2: The Sandbox Wrapper**
Because running analysis tools on suspicious binaries is risky, you must run your analysis script in an isolated environment.
Create a wrapper script at `/home/user/run_sandbox.sh`. This script must use `bwrap` (Bubblewrap) to execute your `audit_script.sh` with the following restrictions:
- No network access (use the appropriate `bwrap` flag to unshare the network namespace).
- Mount `/usr`, `/bin`, `/lib`, and `/lib64` as read-only.
- Mount `/home/user` as read-write.
- Create a bare `/dev` (using the standard `bwrap` flag for this).
- Do not mount anything else (no `/proc`, no `/sys`, etc.).
- The command executed inside the sandbox should be `/home/user/audit_script.sh /home/user/auth.log /home/user/binaries`.

Once both scripts are written, make them executable and run `/home/user/run_sandbox.sh`. 

The system already has Bubblewrap, readelf, and standard coreutils installed.