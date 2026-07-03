You are a forensics analyst responding to a breach on a compromised Linux host. The incident response team has isolated the web server logs, but the web application was completely wiped by the attacker. You need to analyze the proxy logs to determine exactly how the attacker bypassed authentication.

You have been provided with a custom proxy log file located at `/home/user/proxy_logs.txt`. The log format is:
`IP_ADDRESS - [TIMESTAMP] "METHOD PATH HTTP_VERSION" STATUS_CODE "HEADERS_JSON" "COOKIES_JSON"`

Your task is to write a C++ program named `/home/user/analyzer.cpp` that parses this log file, correlates the requests, and identifies the attacker based on their authentication bypass flow.

The attacker's behavior follows this specific pattern:
1. They attempted to access a sensitive path starting with `/admin/` and received a `403 Forbidden` status.
2. They subsequently manipulated both an HTTP header and a cookie to trick the backend into granting them access, resulting in a `200 OK` status on the same sensitive path.
3. The bypass required *both* a forged internal IP header and an elevated privilege cookie.

Your C++ program must:
1. Parse the log file.
2. Identify the attacker's IP address.
3. Identify the sensitive path they successfully accessed.
4. Extract the exact forged header key-value pair that allowed the bypass (the header that was added or modified compared to their first failed request).
5. Extract the exact forged cookie key-value pair that was used in the successful request.
6. Write these findings to `/home/user/forensic_report.txt` in the following strict format:

```
Attacker IP: <ip_address>
Target Path: <path>
Bypass Header: <header_key>: <header_value>
Forged Cookie: <cookie_key>=<cookie_value>
```

Compile and run your C++ program to generate the `/home/user/forensic_report.txt` file. Make sure the output format perfectly matches the requirements.