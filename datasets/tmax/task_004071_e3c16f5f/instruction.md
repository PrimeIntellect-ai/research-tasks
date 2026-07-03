You are an incident responder and forensics analyst assigned to investigate a compromised Linux server. The attacker left behind several artifacts. You need to analyze the evidence, secure the SSH configuration, and write a robust redaction tool for the exfiltrated data.

You must complete the following steps using bash and standard Linux utilities:

1. **Extract Evidence from Image**: The attacker left a screenshot of their terminal at `/app/screenshot.png`. Use OCR (e.g., `tesseract`) to extract the text from this image. Identify the backdoor port number mentioned in the text.
2. **Network Audit**: A snapshot of the system's network connections was taken at the time of the breach and saved at `/home/user/netstat.log`. Find the established connection on the backdoor port you identified in Step 1. Extract the remote (external) IP address connected to this port and save it strictly as a single IPv4 string in `/home/user/attacker_ip.txt`.
3. **SSH Hardening**: The attacker modified the SSH configuration to maintain access. A copy of the compromised config is at `/home/user/sshd_config_compromised`. Create a hardened version at `/home/user/sshd_config_fixed` by ensuring the following settings are exactly as specified (replace existing directives or append if missing):
   - `PermitRootLogin no`
   - `PasswordAuthentication no`
   - `X11Forwarding no`
   - `Protocol 2`
4. **Data Redaction Script (Scored)**: The attacker staged a data dump containing Sensitive PII. You must write a bash script at `/home/user/redact_pii.sh` that takes an input file as its first argument (`$1`) and writes a redacted version to the output file specified by the second argument (`$2`). 
   The script must replace the following patterns with the exact string `[REDACTED]`:
   - Social Security Numbers in the format `XXX-XX-XXXX`
   - Credit Card Numbers in the format `XXXX-XXXX-XXXX-XXXX`
   - Credit Card Numbers as contiguous 16 digits `XXXXXXXXXXXXXXXX`
   *(Assume X is any digit 0-9. Make sure to only match these precise formats using word boundaries so you don't accidentally redact standard log identifiers or timestamps).*

Your redaction script will be evaluated against a hidden, massive dataset of exfiltrated logs. An automated verifier will measure the exact line-by-line accuracy of your redaction against a ground-truth reference file. Your script must process the file correctly and efficiently using standard bash tools (like `sed`, `awk`, or `grep`).