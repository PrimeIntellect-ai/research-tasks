As a compliance analyst, you are tasked with generating an audit trail report for an internal system to identify potential privilege escalation vulnerabilities and access control misconfigurations. 

You have been provided with an authentication dump and a set of user profiles.
- `/home/user/auth_dump.txt`: Contains a list of encoded authentication tokens (one per line).
- `/home/user/profiles/`: A directory containing user profile configurations in the format `<username>.json`.

The authentication tokens are encoded using a proprietary mechanism:
1. The original payload is a JSON object with the fields `user` (string), `role` (string), and `uid` (integer).
2. The JSON string was XOR'd with the static single-byte key `0x5A`.
3. The resulting byte array was then Base64 encoded.

Your task:
1. Write a Go program (e.g., `/home/user/audit.go`) that reads and decodes the tokens from `/home/user/auth_dump.txt`.
2. Analyze the decoded JSON payloads to identify privilege escalation anomalies. A token is considered anomalous if the `role` is `"admin"` but the `uid` is greater than `0`.
3. For each anomalous user identified, check their corresponding profile file in `/home/user/profiles/<username>.json`. You must determine if this file is "world-writable" (i.e., others have write permissions, such as in `0666`).
4. Generate an audit trail report located at `/home/user/escalation_audit.csv`.

The CSV must have the following exact header and format, sorted alphabetically by username:
```csv
Username,UID,WorldWritable
<username>,<uid>,<true/false>
```
*Note: `WorldWritable` should be the boolean string `true` if the file has world-write permissions, and `false` otherwise.*

Ensure your Go program successfully compiles, runs, and produces the required CSV file.