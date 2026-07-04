You are a security auditor tasked with reviewing a set of artifacts from a recently compromised Linux server. You must analyze the artifacts to identify SSH misconfigurations, potential privilege escalation vectors, and a Command Injection vulnerability (CWE-78) in a custom monitoring binary. 

You must write a Go program at `/home/user/generate_report.go` that performs this analysis (or aggregates findings you discover manually via bash utilities) and outputs a final JSON report to `/home/user/audit_report.json`.

The artifacts are located in `/home/user/artifacts/`:
1. `/home/user/artifacts/authorized_keys`: A standard SSH authorized_keys file. You must identify the line numbers (1-indexed) of any keys that use the deprecated `ssh-dss` algorithm.
2. `/home/user/artifacts/file_perms.json`: A JSON file containing an array of objects representing file metadata. Each object has `path` (string), `owner` (string), and `mode` (string, octal representation, e.g., "0644", "4755"). You must identify the `path` of all files that represent a privilege escalation risk. A file is a risk if it has the SUID bit set (mode >= 4000) OR is world-writable (the last octal digit is 2, 3, 6, or 7).
3. `/home/user/artifacts/sys_monitor`: A compiled Go binary. It contains a hidden, hardcoded OS command execution that uses an unsanitized environment variable, leading to CWE-78. You must use basic reverse engineering/disassembly tools (like `strings`, `objdump`, or `nm`) to extract the exact base command string that is passed to `bash -c`.

Your Go program (`/home/user/generate_report.go`) must be compiled and executed. It should output the results to `/home/user/audit_report.json` with the exact following JSON structure:

```json
{
  "weak_ssh_key_lines": [ <int>, <int> ],
  "privesc_files": [ "<path1>", "<path2>" ],
  "cwe78_injected_command": "<the exact hardcoded command string passed to bash -c before the environment variable is appended>"
}
```

Ensure the arrays are sorted in ascending order (numeric for lines, alphabetical for paths).