You are acting as a forensics analyst tasked with recovering exfiltrated evidence from a compromised web server. 

An attacker exploited an open redirect vulnerability in our login flow (`/login?next=...`) to steal encrypted session cookies. We have a packet capture / log export of the traffic, and a screenshot left behind by the attacker on the server.

Your task consists of three phases:

**Phase 1: Evidence Extraction**
1. Inspect the image `/app/attacker_screenshot.png`. It contains a screenshot of the attacker's terminal. Use OCR (e.g., `tesseract`) to extract the initialization seed the attacker used for their encryption script. 
2. Parse the web server logs located at `/app/access.log`. Identify all requests that exploit the open redirect vulnerability (requests to `/login` where the `next` parameter redirects to an external domain `http://evil-attacker.net/...`).
3. Extract the `exfil_data` parameter from these malicious redirect URLs. These are hex-encoded, encrypted session cookies.

**Phase 2: Cryptanalysis and Recovery (Rust)**
The attacker used a custom, weak stream cipher to encrypt the stolen cookies before exfiltrating them in the URL. 
The cipher operates as follows:
- It uses a Linear Congruential Generator (LCG) to generate a keystream.
- The LCG formula is: `X_{n+1} = (1103515245 * X_n + 12345) mod 2^31`.
- The initial state `X_0` is the numeric seed extracted from the image in Phase 1.
- For each byte of the plaintext cookie, the keystream byte is the lower 8 bits of the current LCG state `X_{n+1}`. The ciphertext byte is `plaintext_byte XOR keystream_byte`.
- The LCG state is reset to `X_0` for *each* new cookie exfiltrated.

Write a Rust program in `/home/user/recovery_tool` that takes the extracted hex-encoded ciphertexts, decrypts them using the LCG stream cipher, and outputs the plaintext cookies.
Write the recovered plaintext cookies to `/home/user/recovered_cookies.txt`, one per line, corresponding to the order they appear in the log file.

**Phase 3: Network Policy**
Identify the IP address of the attacker (the single IP that initiated the malicious open redirect requests). Create a bash script at `/home/user/block_attacker.sh` that contains the exact `iptables` command to drop all incoming TCP traffic from this IP address.

**Constraints:**
- Your Rust code must be compiled and executed to produce `/home/user/recovered_cookies.txt`.
- Your work will be evaluated based on the accuracy of your recovered cookies. You must achieve an accuracy metric of >= 0.95 (95%) against the known ground-truth dataset of exfiltrated cookies.