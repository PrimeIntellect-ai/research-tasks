You are an incident responder investigating a compromised Linux server. We have discovered a suspicious stripped binary left by the attacker at `/app/c2_auth`. Forensic analysis indicates this binary acts as a token generator for their command-and-control (C2) authentication.

We also recovered a snippet of a network log showing the attacker successfully authenticating with the following hexadecimal token: `7e82e88d1d86e100f7ef82283ccb3c07`

Your task is to analyze the compromised system, reverse-engineer the attacker's authentication mechanism, and deploy a secure Bash-based honeypot to intercept further attacker connection attempts.

Here are your specific requirements:

1. **Cryptanalysis & Brute-Force:**
   The binary `/app/c2_auth` takes a 4-digit numeric PIN as a single command-line argument and prints an authentication token to stdout. Use Bash and standard CLI tools to brute-force the binary and find the exact 4-digit PIN that generates the token `7e82e88d1d86e100f7ef82283ccb3c07`. 
   Save this 4-digit PIN to `/home/user/cracked_pin.txt`.

2. **Honeypot Implementation:**
   Write a Bash script at `/home/user/honeypot.sh` that simulates the attacker's expected service but traps them.
   - The script must read a single line of input from standard input (simulating the received PIN).
   - If the inputted PIN exactly matches the cracked PIN from step 1, the script must output exactly: `ACCESS_DENIED_HONEYPOT`
   - If the inputted PIN does not match, the script must output exactly: `INVALID_PIN`
   - The script must be executable.

3. **Service Deployment (Process Isolation):**
   Use `socat` to bind your `/home/user/honeypot.sh` script to TCP port `9000` so that any incoming TCP connection to port 9000 automatically executes your script to handle the connection. 
   Run this `socat` listener in the background so it remains active.

Ensure your `socat` command is running and listening on port 9000 before you finish. The automated verifier will connect to `127.0.0.1:9000`, send various 4-digit PINs, and verify the responses.