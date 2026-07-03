You are an incident responder investigating a recent breach on a web application server. We have gathered some evidence, but it is currently locked or obfuscated. 

You need to perform the following steps:

1. **Audio Intercept Analysis**: Listen to the intercepted voicemail located at `/app/voicemail_intercept.wav`. It contains an audio snippet of a suspect mentioning the last 4 characters of a compromised password. The first 4 characters are known to be "h4ck". 
2. **Password Cracking**: Use the recovered partial password to brute-force the remaining possibilities and extract the contents of `/app/network_logs.zip`.
3. **Vulnerability Analysis & Redaction**: The extracted logs contain various HTTP requests, some of which contain XSS and SQL injection payloads, as well as sensitive customer data (credit card numbers and SSNs). 
4. **Tool Creation**: You must write a Python script at `/home/user/redact_logs.py` that takes a single string of raw log data as a command-line argument and prints the redacted version to standard output.
   - It must replace any sequence of 13-16 digits (potentially separated by dashes) with `[REDACTED_CC]`.
   - It must replace any sequence matching the pattern `XXX-XX-XXXX` (where X is a digit) with `[REDACTED_SSN]`.
   - It must neutralize any basic HTML tags (`<script>`, `<img>`, etc.) by replacing `<` with `&lt;` and `>` with `&gt;` to mitigate XSS in our log viewer.
5. **Firewall Configuration**: Finally, generate a bash script at `/home/user/block_ips.sh` that uses `iptables` to drop all traffic from any IP address that attempted a SQL injection (identified by the presence of `UNION SELECT` or `OR 1=1` in the extracted logs).

Ensure your Python script `/home/user/redact_logs.py` is executable and perfectly handles the string transformations as described.