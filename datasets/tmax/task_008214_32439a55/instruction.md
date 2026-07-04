You are a security auditor responding to a suspected open redirect exploitation on a web server. 

You have been provided with the following files:
1. `/home/user/access.log`: A custom web server access log. The format is standard combined log format, but with an additional `req_id` field at the very end of each line.
2. `/home/user/headers.json`: A JSON file containing captured HTTP request headers. It is a list of dictionaries, each containing a `req_id` and a `headers` object.
3. `/home/user/policy.json`: A mock network policy file used by the application's internal firewall.

Your task is to:
1. Parse `/home/user/access.log` to identify the IP address of the attacker who successfully exploited an open redirect vulnerability. The vulnerability was triggered by passing an external URL (starting with `http://evil-domain.com`) to the `next` parameter in the `/login` endpoint, resulting in an HTTP 302 status code.
2. Find the corresponding `req_id` for this malicious request.
3. Inspect `/home/user/headers.json` to find the `AuthToken` cookie value used in that specific request. The cookie string may contain multiple key-value pairs separated by semicolons.
4. Write the attacker's IP address and the exact `AuthToken` value to `/home/user/report.txt`, separated by a single space. (Format: `<IP> <AuthToken>`)
5. Update the firewall configuration in `/home/user/policy.json` by adding the attacker's IP address to the `"blocked_ips"` list. Ensure the file remains valid JSON.

You may write a Python script to accomplish this or use shell commands. All output files must be placed in exactly the paths specified.