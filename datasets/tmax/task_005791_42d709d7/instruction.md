You are an incident responder investigating a suspicious host. We suspect a localized Command and Control (C2) server is running hidden on this machine, and we have a network traffic dump from a brief period of time when the attacker interacted with it. 

Your objectives are to find the running service, reverse-engineer its authentication based on the traffic dump, interact with it to retrieve its payload, and identify all attacker IPs.

Here are the details:
1. **Service Auditing**: The rogue service is running locally on a port between `8000` and `8500`. Find which port it is listening on.
2. **HTTP Header & Cookie Inspection**: Analyze the provided traffic dump file at `/home/user/traffic_dump.txt`. The attacker successfully authenticated to the `/api/c2` endpoint on this service and received a `200 OK` response. Identify the specific `Cookie` and custom HTTP Header (starting with `X-`) that were required to achieve this.
3. **Authentication Flow Testing**: Once you have the port, the required cookie, and the custom header, craft an HTTP GET request to `http://127.0.0.1:<PORT>/api/c2`. The service will respond with a JSON object. Extract the value of the `payload` key.
4. **Pattern Matching**: Write a script (Bash, Python, or another tool of your choice) to parse `/home/user/traffic_dump.txt` and extract a comma-separated list of all unique IP addresses that successfully authenticated to `/api/c2` (received a `200 OK`). Sort the IPs in ascending order.

Output your final findings to a log file at `/home/user/investigation_report.txt` using EXACTLY this format:

```text
Port: <the_discovered_port>
Cookie: <the_full_cookie_string_e.g._Name=Value>
CustomHeader: <the_full_custom_header_e.g._X-Name: Value>
Payload: <the_extracted_payload_string>
Malicious_IPs: <IP_1>,<IP_2>
```

Example of the expected format:
```text
Port: 8080
Cookie: SessionToken=xyz123
CustomHeader: X-Access-Code: 999
Payload: base64_encoded_string_here
Malicious_IPs: 192.168.1.100,192.168.1.105
```

Ensure the file `/home/user/investigation_report.txt` is created with the correct information.