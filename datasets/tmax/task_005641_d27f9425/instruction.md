You are a compliance analyst tasked with generating an audit trail from a legacy system component. 

We have a proprietary binary located at `/home/user/legacy_processor`. This binary processes base64-encoded payloads to execute administrative commands. We need to trigger it to execute the `DUMP_AUDIT` command, which will generate a critical compliance log. 

However, the binary requires a 4-digit numeric PIN (e.g., "0000" to "9999") prefixing the command to authorize execution. The payload format before base64 encoding must be exactly:
`[PIN]:[COMMAND]`
(For example, if the PIN is 1234, the decoded payload should be `1234:DUMP_AUDIT`).

The original developers hardcoded the expected PIN's hash into the binary itself using a custom hashing algorithm. The source code is lost, and we only have the stripped ELF binary.

Your objectives are:
1. Analyze the ELF binary `/home/user/legacy_processor` to reverse-engineer the custom hashing algorithm and identify the hardcoded target hash value.
2. Write a C program at `/home/user/bruteforce.c` that brute-forces the 4-digit PIN by implementing the discovered hashing algorithm.
3. Compile and execute your C program to discover the correct PIN.
4. Construct the proper base64-encoded payload and pass it as the first command-line argument to `/home/user/legacy_processor`. If successful, the binary will create `/home/user/audit_trail.log`.
5. Identify the primary CWE (Common Weakness Enumeration) associated with using a hardcoded password/credential in code.
6. Create a final report file at `/home/user/compliance_audit.json` with the following exact JSON structure:
```json
{
  "pin": "<the 4-digit PIN>",
  "payload_base64": "<the base64 encoded payload you passed to the binary>",
  "cwe_id": "CWE-<number>"
}
```

Ensure all paths are absolute and the JSON keys match exactly.