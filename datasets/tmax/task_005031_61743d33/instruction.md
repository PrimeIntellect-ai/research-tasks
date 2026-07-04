You are a Linux systems engineer performing a configuration hardening audit. Since you do not have root access on the target production servers, the configuration files and diagnostic outputs have been securely copied to your local workspace for analysis.

Your task is to write a Python script at `/home/user/analyze_hardening.py` that parses these mock configuration files and extracts specific security-relevant data. 

The audit files are located in `/home/user/sys_audit/` and consist of the following:
1. `etc_passwd`: A copy of the server's `/etc/passwd` file.
2. `postfix_main.cf`: A copy of the Postfix email server configuration file (`main.cf`).
3. `iptables_save.txt`: A dump of the server's firewall rules generated via `iptables-save`.
4. `ping_results.txt`: The output of several connectivity diagnostic tests.

Your Python script must read these files and generate a plain text report at `/home/user/hardening_report.txt` containing exactly four lines, formatted as follows:

- **Line 1:** A comma-separated list of all usernames from `etc_passwd` that have a UID of `0`, *excluding* the standard `root` user. (e.g., `admin,backdoor`)
- **Line 2:** The exact value assigned to `mynetworks` in `postfix_main.cf`. You should extract everything after the `=` sign (stripped of leading/trailing whitespace).
- **Line 3:** The destination port number of any `ACCEPT` rule in `iptables_save.txt` that targets a port strictly greater than `1024`. Assume there is exactly one such anomalous rule. (e.g., `8080`)
- **Line 4:** The total number of successful ping targets in `ping_results.txt`. A target is considered successful if its statistics block contains the string `0% packet loss`. (e.g., `2`)

Ensure your script is executable and runs successfully to produce the required `/home/user/hardening_report.txt` file. Do not include extra text, labels, or formatting in the output file—only the specific extracted values on their respective lines.