You are a security auditor tasked with generating a safe compliance report from a legacy, undocumented firewall auditing tool. 

There is a compiled ELF binary located at `/home/user/audit_tool`. This tool parses firewall rules, but it is known to be insecure: it lacks input sanitization (leading to potential XSS in HTML reports) and often leaks sensitive environment credentials in its output.

Your task:
1. **Reverse Engineer**: Analyze `/home/user/audit_tool` (using tools like `strings`, `objdump`, or `ltrace`) to discover the undocumented environment variable it requires to set the target IP address. 
2. **Scripting**: Write a Bash script at `/home/user/generate_report.sh` that does the following:
   - Sets the discovered environment variable to the IP address `10.0.0.1`.
   - Executes the binary, passing it the firewall configuration file `/home/user/fw_rules.txt` using the required `-f` flag (i.e., `/home/user/audit_tool -f /home/user/fw_rules.txt`).
   - Captures the standard output of the tool.
   - **Sensitive Data Redaction**: Uses standard Unix utilities (like `sed` or `awk`) to find any AWS-style API keys (strings starting with `AKIA` followed by exactly 16 alphanumeric characters, e.g., `AKIAIOSFODNN7EXAMPLE`) and replaces the *entire* key with the word `REDACTED`.
   - **XSS Mitigation**: Replaces all `<` characters with `&lt;` and all `>` characters with `&gt;` to neutralize cross-site scripting payloads present in the firewall rules.
   - Saves the final, sanitized text to `/home/user/audit_report.txt`.

Ensure your script `/home/user/generate_report.sh` is executable and runs successfully without user interaction.