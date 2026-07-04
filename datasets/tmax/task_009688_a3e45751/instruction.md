You are a network engineer inspecting a recent batch of HTTP traffic logs. Our Intrusion Detection System (IDS) flagged a potential XSS injection attack that managed to bypass our Web Application Firewall (WAF). 

The WAF inspection logs have been exported to `/home/user/traffic_logs.json`. We suspect the attacker smuggled the XSS payload inside a base64-encoded cookie, specifically targeting our staging environment by utilizing a custom HTTP header.

Write a Python script to analyze the JSON log file and perform the following:
1. Filter the logs to find only requests where the HTTP header `X-Test-WAF` is set to exactly `"true"`.
2. For these filtered requests, inspect the `Cookie` header. Extract the value of the `session_data` cookie.
3. Base64-decode the `session_data` value.
4. Identify the request where the decoded `session_data` contains an XSS payload (specifically, it will contain the string `<script>`).

Once you have identified the malicious request, output the results to the following files:
- Create `/home/user/attacker_ip.txt` and write the exact `source_ip` of the malicious request into it.
- Create `/home/user/extracted_payload.txt` and write the exact, decoded XSS payload string into it.

The JSON file is an array of objects, where each object has `source_ip`, `method`, `url`, and `headers` (a dictionary of header key-value pairs). Note that the `Cookie` header may contain multiple cookies separated by semicolons (e.g., `uid=123; session_data=...; theme=dark`).