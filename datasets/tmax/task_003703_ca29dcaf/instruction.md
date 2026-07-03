As a monitoring specialist, you are setting up synthetic monitoring to detect a specific network misconfiguration: an SSH server that silently rejects key-based logins and falls back to interactive password prompts without returning an immediate error code.

Since we are testing this in a restricted environment, a mock SSH client has been provided at `/home/user/mock_ssh`. This script simulates the behavior of connecting to the problematic jump host. 

Your task is to implement an active prober in Go and an idempotent deployment script.

Step 1: The Go Synthetic Prober
Create a Go program at `/home/user/probe_ssh.go`. This program must:
1. Execute the mock SSH client using the exact command: `/home/user/mock_ssh jumpuser@jumphost`
2. Act as an "expect" script by reading the interactive standard output of the mock client.
3. If the output contains the exact string `"Public key rejected. Fallback to password."`, your Go program must immediately write an alert to `/home/user/alerts.log`.
4. The alert must be a single line containing exactly this JSON: `{"event":"key_rejected","target":"jumphost"}`
5. The Go program must successfully navigate the rest of the interactive prompt by sending the password `"probe_pass\n"` when prompted with `"password: "` to cleanly exit the mock SSH session (which otherwise hangs).

Step 2: The Idempotent Deployment Script
Create a bash script at `/home/user/deploy.sh` that does the following:
1. Compiles `/home/user/probe_ssh.go` to an executable at `/home/user/probe_ssh`.
2. Creates `/home/user/alerts.log` if it does not exist.
3. Sets the permissions of `/home/user/alerts.log` to exactly `600` (read/write for the owner only).
4. Ensures the script is idempotent (running it multiple times must result in the exact same system state and exit cleanly with code 0).

Constraints:
- Do not modify `/home/user/mock_ssh`.
- Do not run commands as root/sudo.
- Use only the standard library in your Go code (no third-party expect libraries).