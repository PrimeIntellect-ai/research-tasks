You are a compliance analyst responding to a security incident. A recent audit revealed that a web server's login flow was vulnerable to an open redirect. Attackers exploited this to redirect users to a malicious domain (`evil.com`) and steal encrypted session tokens.

Your task is to analyze the web server logs, block the attacker, and cryptanalyze the stolen token to determine the scope of the breach.

You have been provided with the web server log file at `/home/user/access.log`.

**Objectives:**
1. **Network Policy Configuration:** Identify the IP address of the attacker who exploited the open redirect to send a token to `evil.com`. Create a bash script at `/home/user/block_rules.sh` that contains exactly one `iptables` command to drop all incoming traffic from this attacker's IP address. (Format: `iptables -A INPUT -s <IP> -j DROP`). Ensure the script has execution permissions.
2. **Cryptanalysis & Cracking:** The attacker successfully stole a token in the redirect URL. The token is represented as a hex string in the URL parameter. 
   - Our engineers confirm that tokens are encrypted using a weak single-byte XOR cipher.
   - We know that all valid tokens start with the exact plaintext prefix `AUTH_`.
   - Using this known-plaintext vulnerability, deduce the single-byte XOR key.
3. **Decryption:** Write a bash script at `/home/user/decrypt.sh` that takes the hex-encoded ciphertext as an argument, performs the XOR decryption using the recovered key, and outputs the ASCII plaintext.
4. **Audit Trail:** Execute your script and save the fully decrypted token to `/home/user/audit_token.txt`.

Ensure all output files (`block_rules.sh`, `decrypt.sh`, and `audit_token.txt`) are located in `/home/user/`.