You are an incident responder tasked with investigating a recent web server compromise. You have been provided with some artifacts in the `/home/user/incident_data/` directory.

Your goal is to analyze the logs, inspect a dropped binary, and prepare a clean, redacted log file for sharing with the broader security team.

Here is what you need to do:

1. **Log Analysis & Header Inspection**: Read the web access log located at `/home/user/incident_data/access.log`. Identify the IP address of the attacker. The attacker exploited a vulnerability by sending a malicious payload starting with `() { :; };` in the `User-Agent` HTTP header. 

2. **Binary Analysis**: The attacker dropped an ELF executable on the server, a copy of which is located at `/home/user/incident_data/dropped_malware.elf`. Analyze this binary to find the hardcoded Command and Control (C2) IP address. The IP address is stored in plain text near the string `C2_SERVER: `.

3. **Data Redaction**: Create a sanitized version of the access log at `/home/user/redacted_access.log`. In this new file, you must redact all sensitive credentials. Specifically, use a Python script to replace the values of any `session_token=[alphanumeric_value]` with `session_token=REDACTED`, and `password=[alphanumeric_value]` with `password=REDACTED`. Leave all other log content identical to the original.

4. **Reporting**: Write the findings of your investigation to a JSON file at `/home/user/report.json`. The JSON file must have exactly this format:
```json
{
  "attacker_ip": "<IP_FOUND_IN_STEP_1>",
  "c2_ip": "<IP_FOUND_IN_STEP_2>"
}
```

Write and execute a Python script to automate the log parsing and redaction. Ensure all output files are placed exactly at the specified paths.