You are a network security engineer investigating a recent web server compromise. You have captured some traffic during the incident, but it is encrypted via TLS. 

You have the following artifacts to work with:
1. `/app/traffic.pcap`: A packet capture containing the encrypted TLS traffic between a client and the web server.
2. `/app/server.key.enc`: The encrypted RSA private key of the web server.
3. `/app/passphrase.png`: A scanned image of a physical sticky note found on the sysadmin's desk, which contains the passphrase needed to decrypt the server's private key.

Your objectives:
1. **Extract the Passphrase:** Use OCR (e.g., `tesseract`) to read the passphrase from `/app/passphrase.png`.
2. **Decrypt the Key:** Use the extracted passphrase to decrypt `/app/server.key.enc` and obtain the plaintext RSA private key.
3. **Decrypt the Traffic:** Use the plaintext private key to decrypt the TLS traffic in `/app/traffic.pcap`. (Note: The traffic uses an older RSA key exchange cipher suite, so the private key is sufficient to decrypt the payload).
4. **Extract the Payload:** Inside the decrypted HTTP traffic, there is an HTTP 200 OK response containing an HTML document. Extract this HTML payload to `/home/user/index.html`.
5. **Analyze and Secure (CSP):** The HTML document contains several external resources (scripts, images, styles). Some are legitimate, but one is a malicious injected script from a rogue domain. You must analyze the domains in the HTML. Assume domains containing "trusted" or "internal" are safe, while unknown or suspicious domains are malicious.
6. **Generate a CSP:** Write a Python script at `/home/user/generate_csp.py` that, when executed, prints a single valid Content-Security-Policy (CSP) string to standard output. 
    - The CSP must strictly whitelist only the legitimate origins found in the HTML for `script-src`, `img-src`, and `style-src`.
    - It must explicitly block the malicious domain.
    - It must restrict default sources (`default-src 'self'`).

**Verification:**
Your CSP string will be evaluated by a quantitative scoring metric. We will run `/app/evaluate_csp.py "$(python3 /home/user/generate_csp.py)"`. 
The evaluator will parse your CSP and assign a security score between 0 and 100 based on how effectively it enforces the principle of least privilege against the resources found in the traffic, without breaking the legitimate assets. 
You must achieve a **CSP Security Score of 90 or higher**. Iterate on your script until it outputs a policy that meets this threshold.