You are a network security engineer investigating a recent breach. We have intercepted an attacker's audio memo containing details about the attack parameters, and we have a copy of the vulnerable script they targeted.

Your objectives:
1. **Audio Analysis:** Process the audio file located at `/app/incident_report.wav`. Transcribe it to extract the attacker's IP address and the highly sensitive HMAC-SHA256 secret key they leaked.
2. **File Integrity & Vulnerability Auditing:** 
   - Verify the integrity of `/home/user/vulnerable_app.sh` against the SHA256 hash in `/home/user/checksums.txt`. 
   - Analyze `/home/user/vulnerable_app.sh` to identify the primary weakness allowing the attacker to bypass authentication (specifically, accepting tokens with `alg: "none"`). Identify the most specific, applicable CWE (Common Weakness Enumeration) identifier for this flaw. Write the identifier (e.g., `CWE-123`) to `/home/user/cwe_identified.txt`.
3. **Firewall Policy:** Create a text file `/home/user/block_rule.txt` containing the exact `iptables` command required to drop all incoming TCP traffic from the attacker's IP address extracted from the audio.
4. **Build a Bash JWT Filter:** 
   - Write a Bash script at `/home/user/jwt_filter.sh` that reads a single JSON Web Token (JWT) from standard input (`stdin`).
   - The script MUST securely validate the JWT using the secret key extracted from the audio. 
   - It MUST reject any token where the algorithm is `none`, or where the signature is invalid. 
   - Output exactly `ACCEPT` (followed by a newline) to `stdout` if the token is valid and authenticated. Output exactly `REJECT` (followed by a newline) if the token is forged, tampered with, uses the `none` algorithm, or is otherwise invalid. 
   - Make sure your script is executable (`chmod +x`). 

You will need to ensure your `jwt_filter.sh` script is robust against adversarial inputs. We will test it against a hidden corpus of clean and evil tokens.