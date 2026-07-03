You are a forensics analyst investigating a compromised Linux host. The attacker managed to exploit a vulnerability in a custom local web application, executed arbitrary commands, and left behind a persistence mechanism. 

You need to write a Python script at `/home/user/analyze.py` that performs the forensic analysis and outputs a JSON report.

The system contains the following files:
1. `/home/user/vulnerable_app.py`: The source code of the compromised Python web application.
2. `/home/user/access.log`: The web server access logs.
3. `/home/user/evidence/`: A directory containing files extracted from the compromised system.

Your Python script (`/home/user/analyze.py`) must do the following when executed:
1. **Code Auditing (CWE):** Analyze `vulnerable_app.py` to identify the primary vulnerability class that allowed the attacker to execute arbitrary system commands. Identify its standard MITRE CWE ID (e.g., CWE-79, CWE-89).
2. **Log Analysis (Pattern Matching):** Parse `/home/user/access.log` to find the IP address of the attacker who actively exploited this specific vulnerability. Look for the HTTP request that abuses the vulnerable parameter.
3. **File Permission Analysis:** Scan the `/home/user/evidence/` directory to find the specific file left behind by the attacker that has world-writable permissions (chmod 777).

The script must write the findings to a JSON file at `/home/user/report.json` with the following exact structure:

```json
{
  "cwe": "CWE-XXX",
  "attacker_ip": "X.X.X.X",
  "world_writable_file": "filename.ext"
}
```

Constraints:
- Ensure your Python script runs without errors and successfully creates `/home/user/report.json`.
- The `world_writable_file` field should only contain the base filename (e.g., `backdoor.sh`), not the full path.