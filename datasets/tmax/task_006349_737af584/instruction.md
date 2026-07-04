You are an incident responder investigating a recent compromise on a Linux web server. The attacker leveraged an open redirect vulnerability in the server's authentication flow to deliver a malicious payload and exfiltrate data.

You have been provided with the following artifacts in your home directory (`/home/user/`):
1. `access.log`: The web server access logs.
2. `suspicious_bin`: An ELF executable left behind by the attacker.
3. `stolen_data.enc`: An encrypted file containing the exfiltrated data.

Your task is to investigate the incident and recover the stolen data.

Perform the following steps:
1. **Analyze the Logs**: Identify the IP address of the attacker who exploited the open redirect vulnerability. The vulnerability exists on the `/login` endpoint via the `next` parameter, which the attacker used to redirect the victim to `http://evil.corp/malware`. Write the attacker's IP address to `/home/user/attacker_ip.txt`.
2. **Analyze the Binary**: The attacker used a custom tool (`suspicious_bin`) to encrypt the exfiltrated data. Analyze this ELF binary to find the encryption key. The key is hardcoded in the binary's readable strings and is prefixed with the identifier `KEY:`.
3. **Decrypt the Data**: The attacker used a simple repeating XOR cipher to encrypt `stolen_data.enc` with the key found in step 2. Write a Python script to decrypt `stolen_data.enc` and output the plaintext to `/home/user/decrypted_data.txt`.

Ensure your final output files (`/home/user/attacker_ip.txt` and `/home/user/decrypted_data.txt`) contain only the requested data, with no additional formatting or whitespace.