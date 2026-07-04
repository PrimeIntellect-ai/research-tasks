You are acting as a penetration tester auditing a set of internal local web services. Several web services are running on `localhost` in the port range `8000` to `8500`.

Your objective is to audit these services, extract specific security flags, and generate a final report. 

Here are your instructions:
1. **Service Auditing & Port Scanning:** Scan `localhost` between ports `8000` and `8500` to find exactly two running web services.
2. **Certificate Validation:** One of the services is running over HTTPS with a custom SSL certificate. Connect to this service and extract the `Organization` (O) field from the Subject of its SSL certificate. Save the exact string value of the Organization field to a file named `/home/user/cert_flag.txt`.
3. **Password Cracking:** The other service is running over standard HTTP and is protected by HTTP Basic Authentication. The username is `admin`. You have been provided a wordlist at `/home/user/wordlist.txt`. Use this wordlist to brute-force the password. Once you have the correct password, make an authenticated GET request to the root path (`/`) of the service. The server will respond with a secret text flag. Save this exact flag to `/home/user/auth_flag.txt`.
4. **Summary Report:** Create a JSON file at `/home/user/pentest_summary.json` with the following structure:
```json
{
  "https_port": <integer>,
  "http_port": <integer>,
  "cracked_password": "<string>"
}
```

Ensure all output files (`/home/user/cert_flag.txt`, `/home/user/auth_flag.txt`, `/home/user/pentest_summary.json`) are created successfully with the correct values. You may use any language or standard Linux tools (e.g., `curl`, `nmap`, `openssl`, Python) to complete this task.