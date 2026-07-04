You are a security auditor tasked with verifying the data integrity, authentication mechanisms, and network policies of a simulated data ingestion proxy. 

All files you need are located in `/home/user/audit/`. You must perform the following auditing tasks and consolidate your findings into a single JSON report at `/home/user/audit_report.json`.

**Task 1: Cryptographic Hash and Token Validation**
You have been provided a JSON file containing ingested data logs at `/home/user/audit/logs.json`. Each log entry contains:
- `id`: A unique string identifier.
- `payload`: The raw data string.
- `checksum`: A SHA256 hex digest of the `payload`.
- `token`: An HMAC-SHA256 hex digest of the string `{id}:{payload}` using a shared secret.

The shared secret key is stored in plain text at `/home/user/audit/secret.key`.
Your task is to identify which log entries have been tampered with. A log entry is considered invalid if EITHER its SHA256 `checksum` is incorrect, OR its HMAC-SHA256 `token` is incorrect (or both).

**Task 2: TLS Certificate Management**
The proxy uses a TLS certificate located at `/home/user/audit/proxy.crt`. 
Inspect this certificate to extract:
1. The Subject Common Name (CN).
2. The Expiration Date ("Not After" timestamp) formatted exactly as an ISO 8601 string in UTC (e.g., `2025-12-31T23:59:59Z`).

**Task 3: Firewall Policy Review**
A dump of the firewall rules is located at `/home/user/audit/iptables.dump`.
Analyze these rules to determine if inbound (ingress) traffic to TCP port `8443` is explicitly allowed from the subnet `10.0.50.0/24`. 

**Final Output**
Create a JSON file at `/home/user/audit_report.json` with exactly the following structure:

```json
{
  "invalid_log_ids": [
    "id1",
    "id2"
  ],
  "certificate_cn": "extracted_common_name",
  "certificate_expiration": "YYYY-MM-DDThh:mm:ssZ",
  "firewall_allows_8443_from_subnet": true_or_false
}
```

Notes:
- `invalid_log_ids` must be a sorted list of strings representing the `id`s of the tampered/invalid logs.
- `firewall_allows_8443_from_subnet` must be a boolean (`true` or `false`).
- You may write Python scripts to automate these checks. You have access to standard Python libraries and the `cryptography` package.