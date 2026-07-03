You are an incident responder investigating a potential breach on a Linux system. A suspicious binary and a network traffic log were discovered in the home directory. 

We suspect the attacker downloaded an exploit payload to perform local privilege escalation by targeting an SUID binary.

You have been provided with two pieces of evidence:
1. `/home/user/traffic.log`: A capture of raw HTTP request headers from the compromised server.
2. `/home/user/exploit.elf`: The malicious payload dropped by the attacker.

Additionally, there is a directory of custom local scripts and binaries located at `/home/user/bin/`. One of these files is misconfigured with the SUID bit set, making it a target for privilege escalation.

Your task is to analyze the evidence and determine two things:
1. The attacker authenticated to the C2 server to download the payload. Inspect `traffic.log` and identify the value of the `auth_token` cookie used in the request to `/download_payload`.
2. Analyze the `exploit.elf` binary and audit the local `/home/user/bin/` directory. Identify the exact absolute path to the vulnerable SUID binary that the exploit is targeting. The exploit binary contains strings referencing local paths, but you must verify which of those paths corresponds to a file that actually has the SUID bit set.

Write a Python script or use terminal commands to perform your investigation. Once you have the answers, create a JSON report at `/home/user/findings.json` with the exact following structure:

```json
{
    "auth_token": "<value_of_the_cookie>",
    "target_suid_binary": "<absolute_path_to_the_suid_binary>"
}
```

Make sure the JSON file is perfectly formatted so our automated forensics tool can parse it.