You are a forensics analyst investigating a compromised Linux host. You need to recover a stolen credential flag that is being temporarily exposed by a suspicious binary.

Your investigation has revealed the following:
1. An attacker left behind an audit log at `/home/user/audit.log`.
2. The log contains an encoded payload used to trigger a backdoor in a custom binary located at `/home/user/vuln_service`.
3. When `/home/user/vuln_service` is executed with the decoded payload as its first command-line argument, it temporarily spawns a child process. The stolen flag is passed as an argument to this child process, briefly leaking it in `/proc` before the child process exits (it sleeps for 0.5 seconds).

Your task is to:
1. Parse `/home/user/audit.log` to find the attacker's Base64-encoded payload, and decode it.
2. Write a C program at `/home/user/recover.c` (and compile it to `/home/user/recover`) that automates the recovery. Your program must:
   - Execute `/home/user/vuln_service` with the decoded payload as an argument.
   - Rapidly scan the `/proc` filesystem to find the spawned child process.
   - Read the child process's command line (via `/proc/<pid>/cmdline`) to extract the leaked flag. Note that `/proc/<pid>/cmdline` arguments are null-separated.
   - Write ONLY the extracted flag (e.g., `FLAG{...}`) to `/home/user/recovered_flag.txt`.

Constraints & Requirements:
- You must use C as the primary language for your recovery tool (`/home/user/recover.c`).
- Ensure `/home/user/recovered_flag.txt` contains exactly the flag and nothing else.