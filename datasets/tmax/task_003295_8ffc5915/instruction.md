As a network engineer troubleshooting connectivity and security on a set of legacy jump hosts, you have been tasked with wrapping a vulnerable diagnostic utility and securing the environment.

We have a legacy, interactive network diagnostic shell located at `/app/net_diag_shell`. It is a stripped binary that takes input from standard input (stdin) and performs network checks. However, it is known to be vulnerable to command injections and has undocumented hardcoded restrictions on certain subnets.

Your objectives:
1. **Analyze the Binary:** Interact with or reverse-engineer `/app/net_diag_shell` to determine exactly which inputs it rejects (e.g., restricted management subnets) and which inputs cause shell command injection or unauthorized execution.
2. **Write a Sanitizer:** Create a Python script at `/home/user/sanitize.py` that takes a single command-line argument: the path to a text file containing one diagnostic target per line. 
   - The script must read the file.
   - If *any* line in the file violates the restrictions you discovered or contains shell injection characters, the script must terminate immediately with exit code `1`.
   - If *all* lines are safe and legitimate, the script must terminate with exit code `0`.
3. **System Configuration:**
   - Configure the user's shell profile (`/home/user/.profile`) to export the environment variable `DIAG_ENV=production`.
   - Create a basic shell script at `/home/user/audit.sh` that appends the current date to `/home/user/audit.log`.
   - Configure a cron job for the current user to execute `/home/user/audit.sh` every 5 minutes.

Your Python script (`/home/user/sanitize.py`) will be tested against a hidden suite of clean and malicious input files. It must perfectly distinguish between the two sets based on the rules implemented in the `/app/net_diag_shell` binary.