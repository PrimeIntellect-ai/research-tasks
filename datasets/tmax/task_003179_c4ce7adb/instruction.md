You are acting as a penetration tester analyzing a local system. During your reconnaissance, you discovered a firewall rules export file at `/home/user/iptables.rules` and a custom authentication daemon binary at `/home/user/auth_service`. 

Your objective is to reverse engineer the service, bypass its authentication, and retrieve the secret flag.

Perform the following steps:
1. **Network Policy Analysis:** Inspect `/home/user/iptables.rules`. Find the rule containing the comment `/* auth_service_port */`. Extract the allowed TCP port number.
2. **Binary Analysis & Hashing:** The `auth_service` is an ELF binary. It contains a hardcoded SHA-256 hash in its read-only data section which is used to verify the authentication token. Analyze the binary to extract this 64-character hex string hash.
3. **Authentication Bypass:** The extracted hash corresponds to a 4-digit numeric PIN (ranging from `0000` to `9999`). Crack the hash to find the original 4-digit PIN.
4. **Auth Flow Testing:** Run the daemon locally on the allowed port using the command: `./auth_service <port> &`. Then, test the authentication flow by opening a TCP connection to the service on localhost and sending the cracked 4-digit PIN. If successful, the daemon will respond with a flag.
5. **Reporting:** Compile your findings into a final report located at `/home/user/report.txt`. 

Your `/home/user/report.txt` file must exactly match this format:
```
Port: <port_number>
Hash: <extracted_sha256_hash>
PIN: <cracked_4_digit_pin>
Flag: <flag_string>
```

Replace the bracketed placeholders with your actual discovered values.