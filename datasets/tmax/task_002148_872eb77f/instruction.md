You are a compliance analyst tasked with generating an automated audit trail script for a highly regulated environment. Our security operations center (SOC) exports log data from our code auditing and file integrity monitoring systems. 

You have been given a scanned policy memo at `/app/policy_memo.png`. You must read this image to extract two critical pieces of compliance information:
1. The `CRITICAL_CWE` identifier.
2. The `TRUSTED_HASH` (a SHA256 checksum).

Your task is to write a precise Bash script at `/home/user/audit_parser.sh` that reads security logs from standard input (`stdin`) and categorizes them according to the policy.

The input logs will consist of multiple lines, where each line contains exactly four fields separated by a pipe character (`|`):
`FILE_PATH|FILE_HASH|DETECTED_CWE|AUDIT_MESSAGE`

For each input line, your script must evaluate the fields and print exactly one corresponding output line to standard output (`stdout`), strictly evaluating in the following order of precedence:

1. **Configuration Error:** If the `DETECTED_CWE` field is exactly `CWE-000` (indicating a scanner failure), immediately output: 
   `CONFIG_ERROR|<FILE_PATH>`
   (This overrides all other checks, even integrity violations).

2. **Integrity Violation:** If the `FILE_HASH` does *not* exactly match the `TRUSTED_HASH` extracted from the image, output: 
   `INTEGRITY_VIOLATION|<FILE_PATH>`

3. **CWE Alert:** If the `FILE_HASH` matches the `TRUSTED_HASH`, but the `DETECTED_CWE` exactly matches the `CRITICAL_CWE` extracted from the image, output: 
   `CWE_ALERT|<FILE_PATH>|<AUDIT_MESSAGE>`

4. **Compliant:** If none of the above conditions apply, output: 
   `COMPLIANT|<FILE_PATH>`

Constraints:
- The script must be written entirely in Bash using standard utilities.
- It must handle an arbitrary number of lines piped to standard input.
- Make sure the script is executable (`chmod +x /home/user/audit_parser.sh`).
- Do not output any additional text, headers, or formatting. The automated verification system will test your script against a reference implementation with hundreds of random log entries. Output must be bit-exact.