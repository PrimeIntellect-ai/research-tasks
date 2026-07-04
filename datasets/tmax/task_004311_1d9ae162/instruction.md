You are a penetration tester engaged in a security assessment of a target organization's internal infrastructure. During your enumeration, you discovered a custom, proprietary authentication mechanism. 

The organization uses a compiled, stripped C binary located at `/app/cert_validator` to validate mutual TLS (mTLS) client certificates. You suspect that the developers left a deliberate backdoor in this binary to allow them to bypass authentication during emergencies.

Your objectives are as follows:

1. **Reverse Engineer the Binary:** Analyze the stripped binary at `/app/cert_validator`. Identify the backdoor mechanism. The backdoor is triggered when a specific field within the X.509 certificate's Subject hashes to a specific, hardcoded value.
2. **Crack the Hash:** Once you identify the hash algorithm and the hardcoded digest within the binary, crack it. The original plaintext is a common English dictionary word. Save the cracked plaintext string exactly as it is into a new file at `/home/user/cracked_password.txt`.
3. **Build a Detector:** Write a Bash script at `/home/user/detect_backdoor.sh` that takes exactly one argument: the file path to a PEM-encoded X.509 certificate. 
   - The script must parse the certificate to check if it contains the backdoor payload in the relevant field.
   - If the certificate is designed to trigger the backdoor, your script must print exactly the word `EVIL` to standard output and exit with code 1.
   - If the certificate is normal, your script must print exactly the word `CLEAN` to standard output and exit with code 0.
   - The script must be written primarily in Bash and utilize standard Linux utilities (like `openssl`, `grep`, `awk`, etc.).

Ensure your script is robust and correctly extracts the precise field required by the backdoor logic without being confused by other fields in the certificate. Make sure to set executable permissions on your script.