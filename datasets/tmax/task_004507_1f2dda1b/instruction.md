You are acting as an incident responder investigating a recent breach. An attacker exploited a path traversal vulnerability in our file upload handler to drop malicious payloads into our system. 

We have quarantined the recently uploaded files in the `/home/user/uploads` directory. Most of these files are harmless images or text logs, but we suspect the attacker uploaded a compiled ELF executable disguised with a benign extension to bypass our filters. We also believe this malicious binary contains a hardcoded authentication token used to communicate with the attacker's command and control server.

Your task is to:
1. Analyze the files in `/home/user/uploads` to identify the hidden ELF executable.
2. Extract the hardcoded authentication token from the binary. The token is stored as a string starting with `AUTH_TOKEN=`.
3. Compute the SHA256 hash of the token's value (everything AFTER the `AUTH_TOKEN=` prefix, without a trailing newline).
4. Generate a report in `/home/user/investigation_report.txt` with the exact following format:

```
Suspicious File: <filename_with_extension>
Token: <full_token_string_including_prefix>
Hash: <sha256_hash_of_the_token_value_only>
```

For example, if the file was `data.csv`, the token was `AUTH_TOKEN=secret123`, and the hash of `secret123` is `2bb80d53...`, your report should look like:
```
Suspicious File: data.csv
Token: AUTH_TOKEN=secret123
Hash: 2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b
```

Ensure the file `/home/user/investigation_report.txt` is formatted exactly as specified.