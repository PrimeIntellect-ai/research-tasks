You are an incident responder investigating a potential web server compromise. The security team detected an anomaly in the web application's CGI directory, suspecting an attacker has uploaded a malicious binary to maintain persistence and potentially escalate privileges.

Your task is to analyze the contents of the web directory located at `/home/user/webroot/cgi-bin`. 

Perform the following steps:
1. Identify any compiled ELF binaries in `/home/user/webroot/cgi-bin` that have the SUID (Set Owner User ID) bit set. This is a common privilege escalation vector.
2. Analyze the identified malicious binary using standard Linux binary analysis tools (e.g., `readelf`, `strings`, `objdump`). 
3. Extract the hardcoded backdoor authentication key embedded inside the binary. The key is in the format `AUTH_BYPASS_KEY=<value>`.
4. Document your findings in a JSON-formatted incident report at `/home/user/investigation_result.json`.

The JSON file must have the following exact structure:
```json
{
  "malicious_file": "<absolute_path_to_the_binary>",
  "permissions": "<4-digit_octal_permissions>",
  "hidden_key": "<extracted_value_only_without_AUTH_BYPASS_KEY=>"
}
```

Ensure your JSON is perfectly formatted. Use tools like `find`, `stat`, and `strings` from your Bash terminal to complete this investigation.