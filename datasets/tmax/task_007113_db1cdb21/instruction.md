You are acting as a compliance analyst. You have been provided with a directory of pre-production deployment artifacts in `/home/user/artifacts/`. Your goal is to generate an automated audit trail for these artifacts using a Bash script. 

Write a Bash script at `/home/user/audit.sh` that performs the following compliance checks and generates an audit report at `/home/user/audit_report.json`.

The `/home/user/artifacts/` directory contains:
1. `web_server_daemon` - A compiled ELF binary.
2. `manifest.txt` - A text file containing the expected SHA256 hash of the `.rodata` section of the binary.
3. `server_certs.pem` - A certificate file containing a leaf certificate and an intermediate certificate.
4. `root_ca.pem` - The trusted Root CA certificate.
5. `templates/` - A directory containing static HTML files (`*.html`).

Your script `/home/user/audit.sh` must perform the following actions:
1. **ELF Analysis & Hashing**: Extract the `.rodata` section from `web_server_daemon` as raw binary data, compute its SHA-256 hash, and check if it matches the hash provided in `manifest.txt` (the manifest file contains only the 64-character hex string).
2. **Certificate Validation**: Verify the certificate chain in `server_certs.pem` against the provided `root_ca.pem`. Determine if the chain is valid.
3. **XSS Vulnerability Analysis**: Scan all `.html` files in the `templates/` directory. Count the exact number of files that contain the specific string `eval(` anywhere inside them (this is a rudimentary check for unsafe inline script evaluation).

Finally, your script must output the results as a strictly formatted JSON file at `/home/user/audit_report.json` with the following structure:
```json
{
  "rodata_hash": "<computed_sha256_hash_of_rodata>",
  "hash_match": <true_or_false>,
  "cert_valid": <true_or_false>,
  "xss_vuln_count": <integer_count_of_vulnerable_files>
}
```

Constraints:
- You must use Bash as the primary language for your script. Standard Unix tools (like `objcopy`, `sha256sum`, `openssl`, `grep`, `jq`, etc.) are allowed and expected.
- Run your script once it is written to generate the `audit_report.json` file.