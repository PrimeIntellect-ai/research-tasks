You are acting as a compliance analyst for your organization. You need to generate an automated audit trail report based on some internal security logs and certificate configurations.

You have been provided with a set of files in your home directory (`/home/user/`):
1. `/home/user/certs/ca.crt`: The root Certificate Authority for the internal network.
2. `/home/user/certs/server.crt`: The TLS certificate for the internal web application.
3. `/home/user/logs/waf.log`: A Web Application Firewall (WAF) log file containing recent alerts.

Your task is to write a Bash script named `/home/user/generate_audit.sh` that performs the following steps when executed:
1. **Certificate Chain Validation**: Validate `server.crt` against `ca.crt`.
2. **Subject Extraction**: Extract the subject line from `server.crt`.
3. **Log Correlation**: Parse `waf.log` to identify IP addresses that have triggered **both** `[SQLI]` and `[XSS]` alerts.
4. **Audit Trail Generation**: The script must output a JSON file at `/home/user/audit_report.json` with the exact following format:

```json
{
  "certificate_valid": true,
  "server_cert_subject": "<extracted_subject_string>",
  "threat_ips": [
    "<ip_address_1>",
    "<ip_address_2>"
  ]
}
```

Rules for the JSON output:
- `certificate_valid` should be the boolean `true` if `openssl verify` succeeds, or `false` otherwise.
- `server_cert_subject` must be the exact string output by `openssl x509 -noout -subject -in server.crt` (e.g., `subject=CN = ...` or `CN = ...` depending on your openssl version, just use the exact output of the command but strip the leading `subject= ` if it exists, so it starts with `CN = ` or similar).
- `threat_ips` must be a JSON array of strings containing the unique IP addresses that appear in `waf.log` with both `[SQLI]` and `[XSS]` tags. Sort the IPs in ascending order.

Once you have written `/home/user/generate_audit.sh`, execute it so that `/home/user/audit_report.json` is created.