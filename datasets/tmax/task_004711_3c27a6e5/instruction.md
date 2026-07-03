You are a compliance analyst tasked with generating secure audit trails for our internal services. We have a legacy access control system that obfuscates audit log entries using a repeating-key XOR stream cipher before appending them to the audit trail. 

You have been provided with a scanned snippet of our legacy security policy document at `/app/cert_policy.png`. 

Your task is to:
1. Extract the compliance key from the image. The image contains a line in the format `COMPLIANCE_KEY=<the_key>`.
2. Write a Python script at `/home/user/audit_tool.py` that replicates the legacy system's obfuscation logic.
3. The script must accept exactly one command-line argument (the audit string, which could represent a port scan log, file permission change, or certificate validation event).
4. The script must XOR each character of the input string with the corresponding character of the extracted compliance key. If the input string is longer than the key, the key should cyclically repeat.
5. The script must output the final obfuscated result strictly as a continuous lowercase hexadecimal string, followed by a newline.
6. Ensure the script has the correct file permissions to be executed directly from the shell (`chmod +x`) and includes the appropriate python3 shebang.

Example (assuming the key was `SEC`):
If the input is `test`, the operations are:
't' XOR 'S' -> hex
'e' XOR 'E' -> hex
's' XOR 'C' -> hex
't' XOR 'S' -> hex
Output: concatenated hex string.

An automated verifier will aggressively fuzz your script against a reference binary with hundreds of random payloads to ensure bit-exact equivalence.