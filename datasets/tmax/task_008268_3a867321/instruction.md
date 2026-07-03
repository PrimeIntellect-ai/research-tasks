You are a DevSecOps engineer enforcing security policies as code. An automated pipeline has flagged suspicious activity on a staging server. You must investigate the artifacts, crack a backdoor password, identify tampered files, and write a remediation policy.

You have been provided with the following files:
1. `/home/user/audit/firewall_bypass.go` - A suspicious Go source file found in a recent commit. It appears to act as a backdoor that listens on a specific TCP port when a 4-digit PIN is provided. The PIN is hardcoded as a SHA256 hash.
2. `/home/user/audit/checksums.txt` - A list of approved SHA256 checksums for the compiled binaries running on the server.
3. `/home/user/services/` - A directory containing three binaries: `service_alpha`, `service_beta`, and `service_gamma`.

Perform the following tasks:
1. **Password Cracking:** Analyze `/home/user/audit/firewall_bypass.go`. Extract the SHA256 hash and the port number. Write a Go program at `/home/user/crack.go` that brute-forces the 4-digit PIN (ranging from `0000` to `9999`).
2. **Checksum Verification:** Verify the SHA256 checksums of the three binaries in `/home/user/services/` against `/home/user/audit/checksums.txt`. Identify which binary has been tampered with (its actual hash will not match the hash in the text file).
3. **Firewall Policy:** Write a bash script at `/home/user/remediate.sh` containing a single `iptables` command to append a rule that drops all incoming TCP traffic to the backdoor port you discovered. (Assume standard `iptables` syntax).
4. **Reporting:** Generate a final report at `/home/user/report.txt` with exactly the following format:

```
PIN: <cracked_4_digit_pin>
PORT: <backdoor_port_number>
TAMPERED_BINARY: <name_of_tampered_binary>
```

Replace the bracketed placeholders with your findings.