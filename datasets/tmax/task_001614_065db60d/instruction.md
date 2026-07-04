You are a network engineer analyzing suspicious traffic directed at an internal administrative portal. You have been provided with a JSON log file containing recent HTTP requests. 

The security team suspects an attacker bypassed authentication and injected a malicious binary payload into the system.

Your task is to analyze the traffic dump, identify the malicious request, extract the payload, analyze the binary, and create an incident report.

Here are the details:
1. The traffic log is located at `/home/user/traffic_dump.json`.
2. Inspect the HTTP headers to find the malicious request. The portal uses a custom header `X-Admin-Token` for authentication. A *valid* token is exactly the MD5 hash of the request's `User-Agent` string concatenated with the secret salt `SuperSecretSalt2024`. (e.g., `md5(User-Agent + "SuperSecretSalt2024")`). 
3. One request in the log has an invalid `X-Admin-Token` that does not match this calculation. This is the malicious request.
4. Extract the `body` of this malicious request. Inside the body, you will find an XSS/SQLi payload that contains a hex-encoded ELF executable. The hex string is located exactly between the markers `ELF_START:` and `:ELF_END`.
5. Extract this hex string, decode it into a binary file, and save it as `/home/user/payload.bin`.
6. Analyze the extracted ELF binary (`/home/user/payload.bin`) to find the hardcoded Command and Control (C2) IP address. The IP address is stored as a string in the binary in the format `C2_IP=<IP_ADDRESS>`.
7. Write your findings to `/home/user/investigation.txt` in the following exact format:

```
Malicious Source IP: <IP address from the X-Forwarded-For header of the malicious request>
Forged Token: <The invalid X-Admin-Token value>
C2 Server: <The extracted C2 IP address from the ELF binary>
```

Ensure all steps are completed and `/home/user/investigation.txt` is formatted correctly.