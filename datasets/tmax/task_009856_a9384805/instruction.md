You are a forensics analyst investigating a compromised host. The attacker exploited a path traversal vulnerability in a file upload handler, bypassed WAF rules using XSS payloads in their User-Agent, and sent custom HTTP headers containing file checksums.

You have been provided with:
1. A web server access log at `/home/user/server.log` in JSON Lines format. Each line is a JSON object with the following keys: `ip`, `method`, `path`, `status`, `user_agent`, and `headers` (which is an object of HTTP headers).
2. A directory of recovered files at `/home/user/evidence/`.

Your task is to write a Bash script at `/home/user/analyze.sh` that processes these logs and correlates them with the recovered files to identify the successful attacks.

The script must perform the following:
1. Parse `/home/user/server.log` to find log entries that meet ALL of the following criteria:
   - The HTTP `method` is `POST`.
   - The HTTP `status` is exactly `200`.
   - The `path` contains a path traversal sequence. For this task, look specifically for the literal string `../` or its URL-encoded equivalents `%2E%2E/` or `%2e%2e/`.
   - The `user_agent` contains an XSS injection attempt, specifically indicated by the substring `<script>` (case-insensitive).
2. For each matching log entry, extract the attacker's IP address and the value of the `X-Payload-Hash` header (from the `headers` object).
3. Compute the SHA-256 hashes of all files in `/home/user/evidence/`.
4. Check if the `X-Payload-Hash` extracted from the log matches the SHA-256 hash of any file in the `/home/user/evidence/` directory.
5. If a match is found, record the successful attack.

Your script must output the findings to `/home/user/report.txt`. Each line in the report should correspond to a verified attack and follow this exact format:
`<IP_ADDRESS> <MATCHING_EVIDENCE_FILENAME> <SHA256_HASH>`

The output lines in `/home/user/report.txt` must be sorted alphabetically by the IP address.

Example of a single line in `/home/user/report.txt`:
`192.168.1.100 payload.elf 8b5a...`

Make sure `/home/user/analyze.sh` is executable and run it to produce the final `report.txt`.