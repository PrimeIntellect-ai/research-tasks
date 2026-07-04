You are a DevSecOps engineer tasked with enforcing policy as code after a recent security incident. We suspect attackers have been exploiting an open redirect vulnerability in our web application's login flow to steal credentials, and then attempting to access our servers via SSH.

Your task is to write a Python script located at `/home/user/enforce.py` that performs the following actions:

1. **Security Log Parsing & Correlation:**
   Read the web access log located at `/home/user/logs/gateway.log`. The log follows a standard format but includes the requested URI and the HTTP response status. 
   Find all unique IP addresses that successfully exploited the open redirect. An exploit is successful if the request was made to the `/login` endpoint, the HTTP response status is `302`, and the `next` query parameter contains an absolute URL (starts with `http://` or `https://`). Ignore requests where `next` is a relative path (e.g., `/dashboard`) or if the status code is not `302`.

2. **SSH Hardening:**
   For every malicious IP address identified in step 1, generate an SSH daemon configuration snippet to block them. 
   Write these directives to `/home/user/ssh_deny.conf`. The file must contain exactly one line per IP in the following format, sorted in ascending alphabetical/lexicographical order:
   `DenyUsers *@<IP_ADDRESS>`

3. **Content Security Policy (CSP) Enforcement:**
   To mitigate further risks in the login flow, we need to harden our HTTP headers. Read the current CSP string from `/home/user/csp.txt`. 
   Parse this CSP and ensure the `form-action` directive is strictly set to `'self'`. If `form-action` exists, replace its value with `'self'`. If it does not exist, append `; form-action 'self'` to the end of the policy (ensuring proper spacing and semicolon separation). 
   Write the resulting hardened CSP string to `/home/user/hardened_csp.txt`.

You may use standard Python libraries. Do not use external libraries that require `pip install`. Make sure you run your script to generate the required output files before finishing.