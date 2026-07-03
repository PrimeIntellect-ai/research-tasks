As an incident responder, you are investigating a potentially compromised system and a set of suspicious logs. You need to perform system auditing, vulnerability scanning, and fix a custom C++ log processing tool. 

Please complete the following objectives:

1. **Privilege Escalation Auditing**: 
   Write a bash script at `/home/user/audit_privesc.sh` that searches the directory `/home/user/suspicious/` (and its subdirectories) for any files that have the SUID bit set OR are world-writable. The script should output the absolute paths of these files to `/home/user/audit_report.txt`, one file per line, sorted alphabetically. Execute the script to generate the report.

2. **Automated Vulnerability Scanning**:
   Install the `cppcheck` tool (using `sudo apt-get update && sudo apt-get install -y cppcheck`). Run it against the source code located in `/home/user/log_analyzer/src/`. Save the output report in XML format to `/home/user/vuln_report.xml` (use the `--xml` flag).

3. **Code Remediation (C++)**:
   The custom log analyzer in `/home/user/log_analyzer/src/main.cpp` is broken. It is supposed to parse `/home/user/data/input.log`, validate certificate chains, redact sensitive data, and write the cleaned logs to `/home/user/data/clean_output.log`.
   Fix the C++ code to implement the following logic:
   - **Certificate Chain Validation**: Each log line contains a certificate chain labeled as `CHAIN: ` followed by a comma-and-space-separated list of certificates, where each certificate is formatted as `Subject|Issuer` (e.g., `Client1|IntCA1, IntCA1|RootCA`). 
     A chain is considered *valid* if:
     a) For any adjacent certificates, the Issuer of the first is exactly the Subject of the next.
     b) The final certificate's Issuer is exactly the string `"RootCA"`.
     If a line has an *invalid* chain, the analyzer must completely omit that line from the output.
   - **Sensitive Data Redaction**: In the remaining valid lines, find any continuous 16-digit numeric sequences (representing credit card numbers) and replace the first 12 digits with asterisks (`*`), leaving only the last 4 digits visible (e.g., `1234567812345678` becomes `************5678`).
   - The original formatting of the valid log lines must be preserved (other than the redacted numbers).

4. **Compilation and Execution**:
   Compile your fixed C++ code using:
   `g++ -std=c++17 -o /home/user/log_analyzer/bin/analyzer /home/user/log_analyzer/src/main.cpp`
   Run the compiled binary to process `/home/user/data/input.log` and generate `/home/user/data/clean_output.log`.