You are a network engineer analyzing a suspicious authentication mechanism captured on your internal network. 

I have saved an excerpt of the captured traffic logs in `/home/user/traffic.log`. 

Each line in the log represents an authentication request and contains a timestamp, the source IP, the username, and the hexadecimal authentication token. Upon initial inspection, it appears the token is generated using a repeating-key XOR cipher applied directly to the ASCII values of the username. 

Your task is to:
1. Extract the usernames and their corresponding tokens from `/home/user/traffic.log` using pattern matching.
2. Perform a known-plaintext attack (cryptanalysis) to deduce the secret XOR key used by the authentication service.
3. Once you have recovered the key, craft a malicious authentication payload (token generation) for the highly privileged username: `admin_root`.
4. Write your exploit payload exactly in the format `admin_root:<FORGED_TOKEN>` to the file `/home/user/forged_payload.txt`. Ensure the token is in lowercase hexadecimal format (2 hex characters per byte).

You may use Python or bash command-line tools to solve this. Ensure `/home/user/forged_payload.txt` contains exactly one line with your final crafted payload.