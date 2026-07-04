I need you to act as a security auditor. We have a directory of legacy Python administration scripts in `/home/user/scripts/` that are executed by a privileged cron job. We suspect these scripts contain security flaws, specifically command injection vulnerabilities and credential leakage (e.g., passing passwords as cleartext command-line arguments that would be visible to all users via `/proc`).

Your task is to build a static analysis auditing tool in Python, located at `/home/user/audit_tool.py`, that scans all `.py` files in a given directory for these vulnerabilities. 

The tool must use Python's `ast` module (Abstract Syntax Trees) or robust regular expressions to detect the following patterns:
1.  **Credential Leakage**: Any use of `subprocess.run`, `subprocess.Popen`, `subprocess.call`, or `os.system` where a variable named `password`, `token`, `secret`, or `api_key` is passed directly into the command arguments (either as a string concatenation, f-string, or list element).
2.  **Command Injection**: Any use of `os.system` that interpolates external variables (e.g., f-strings or `.format()`) into the command string.

Your script must take the target directory as a command-line argument:
`python3 /home/user/audit_tool.py /home/user/scripts/`

The tool must generate a JSON report at `/home/user/audit_report.json` with the following exact structure:
```json
{
  "scanned_files": 3,
  "vulnerabilities": [
    {
      "file": "/home/user/scripts/example.py",
      "type": "credential_leakage",
      "line_number": 14
    },
    {
      "file": "/home/user/scripts/example.py",
      "type": "command_injection",
      "line_number": 22
    }
  ]
}
```
*Note: Sort the `vulnerabilities` list alphabetically by `file` name, then by `line_number` in ascending order.*

Run your tool against `/home/user/scripts/` and ensure the `audit_report.json` is generated correctly.