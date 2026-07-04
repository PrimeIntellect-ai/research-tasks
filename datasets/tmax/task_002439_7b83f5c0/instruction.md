As a compliance analyst, I am generating an audit trail for a recent security breach. We suspect an attacker bypassed our custom legacy authentication daemon. 

We have a backup of the proprietary authentication daemon, which is a stripped ELF binary located at `/app/legacy_auth`. We also have an HTTP access log with correlated authentication tokens located at `/var/log/auth_headers.log`. 

Your task is to:
1. Analyze the `/app/legacy_auth` binary to understand its custom token generation algorithm. The binary takes a username, a password, and a UNIX timestamp, and outputs an authentication token. 
2. Inspect the HTTP logs in `/var/log/auth_headers.log`. Each line contains a JSON payload with a `timestamp`, `username`, and `X-Auth-Token` header used during the breach.
3. Write a high-performance Go program at `/home/user/recover_passwords.go` that takes a log file path as its first argument, a wordlist file path as its second argument, and an output JSON file path as its third argument.
4. Your Go program must parse the logs, generate candidate tokens using the algorithm you reverse-engineered (using the provided timestamps and candidate passwords from the wordlist), and output a JSON dictionary mapping each `username` to their recovered `password`.

For your testing, use the wordlist at `/usr/share/wordlists/rockyou-top500.txt`. 

When you are done, ensure `/home/user/recover_passwords.go` compiles and runs successfully. Automated compliance verifiers will test your Go source code against a completely different set of held-out logs to measure its password-recovery accuracy.