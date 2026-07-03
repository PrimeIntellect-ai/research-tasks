You are a security engineer preparing to rotate critical authentication credentials for an internal web service. Before completing the rotation, you need to audit the existing environment to ensure the old credentials haven't been actively exploited and to identify any misconfigurations. 

You have been provided with three files in `/home/user/audit_data/` capturing the state of the old service:
1. `/home/user/audit_data/headers.txt`: A raw dump of the HTTP response headers from the old service API.
2. `/home/user/audit_data/service.log`: An access log of recent requests to the service. The format is standard combined log format, with the authentication token appended at the very end of each line inside double quotes.
3. `/home/user/audit_data/scan.nmap`: The output of a recent Nmap port scan of the service host.

Your task is to write a Rust program that analyzes these files and generates a security audit report. 

Requirements for your Rust program:
1. **Header Inspection:** Parse `headers.txt` to extract the value of the `X-Old-Cred-Token` header. This is the leaked credential that needs rotating.
2. **Log Parsing & Correlation:** Parse `service.log`. Find all unique IP addresses (the first field in the log line) that successfully made a request (HTTP status code `200`) using the exact leaked token found in step 1.
3. **Service Auditing:** Parse `scan.nmap`. Extract all open port numbers. The only authorized open ports are `22`, `80`, and `443`. Any other open port is considered unauthorized.
4. **Output Generation:** Your Rust program must output a JSON file to `/home/user/audit_report.json` with the following exact structure:

```json
{
  "leaked_token": "<token_string>",
  "compromised_ips": ["<ip1>", "<ip2>"],
  "unauthorized_ports": [<port1>, <port2>]
}
```

Constraints for the output JSON:
- `compromised_ips` must be an array of strings, sorted alphabetically.
- `unauthorized_ports` must be an array of integers, sorted in ascending numerical order.

You may create a Cargo project or use a single `main.rs` file, but you must compile and run your Rust program to generate the final `/home/user/audit_report.json` file. Use standard CLI tools and standard Rust libraries (or add dependencies via Cargo if you create a project).