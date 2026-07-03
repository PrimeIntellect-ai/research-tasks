You are an incident responder investigating a compromised SSH authentication flow on a Linux server. The attacker left behind a bundle of certificates and a modified authentication helper binary. The incident data is located in `/home/user/incident/`.

Your objective is to analyze the artifacts and extract the attacker's hidden credentials using Bash commands and standard Linux utilities.

1. **Certificate Chain Validation:**
   The file `/home/user/incident/chain.pem` contains a chain of X.509 certificates. One of the certificates in this chain is expired. Find the expired certificate, extract its Subject Common Name (CN), and write the CN (just the value, e.g., `example.com`) to `/home/user/expired_cn.txt`.

2. **Binary and Token Analysis:**
   The attacker replaced the standard SSH helper with a malicious ELF binary located at `/home/user/incident/auth_helper`. 
   The attacker embedded a backdoor authentication token inside a custom ELF section named `.backdoor`.
   - Extract the raw contents of the `.backdoor` section from the `auth_helper` binary.
   - The extracted content is a token formatted similarly to a JWT: `Base64(Header).Base64(Payload).Base64(Signature)`.
   - Extract the Payload portion (the middle segment), decode it from Base64, and write the decoded JSON string exactly as it decodes to `/home/user/backdoor_payload.json`.

Ensure your final files contain exactly the requested strings with no additional formatting or text.