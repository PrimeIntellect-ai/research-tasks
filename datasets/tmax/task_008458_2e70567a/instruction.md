You are an incident responder investigating a recent security breach on a Linux server. The server hosts a Python-based web application that was allegedly exploited to drop a malicious payload.

You have been provided with two pieces of evidence:
1. The web application source code located at `/home/user/webapp.py`
2. The web server access logs located at `/home/user/access.log`

Your task is to analyze these files to understand the attack chain. You will need to write and execute Python scripts or shell commands to parse the logs, extract and decode the attacker's payload, analyze the resulting binary, and audit the application code to identify the vulnerability.

Perform the following steps:
1. **Code Audit**: Analyze `/home/user/webapp.py` to identify the specific Common Weakness Enumeration (CWE) identifier of the vulnerability that allowed the attacker to execute arbitrary commands.
2. **Log Analysis & Payload Decoding**: Inspect `/home/user/access.log` to find the malicious request. The attacker injected a base64-encoded ELF binary into a URL parameter, along with commands to decode and execute it. Extract this base64 string, decode it, and save the resulting binary file.
3. **Binary Analysis**: Analyze the decoded ELF binary to determine its ELF Class (e.g., ELF32, ELF64) and extract the hardcoded Command and Control (C2) IP address embedded within it.

Once you have gathered this information, generate a JSON report at `/home/user/incident_report.json` with the following precise structure and keys:
```json
{
  "attacker_ip": "<The IP address of the attacker found in the access log>",
  "cwe_number": "<The standard CWE identifier for the vulnerability, e.g., CWE-79, CWE-89, CWE-78>",
  "c2_server": "<The hardcoded C2 IPv4 address found inside the decoded ELF binary>",
  "elf_class": "<The class of the ELF file, e.g., ELF32 or ELF64>"
}
```

Ensure the JSON file is valid and strictly adheres to the requested keys. You may use standard Linux utilities (`base64`, `readelf`, `strings`, etc.) and Python to accomplish this task.