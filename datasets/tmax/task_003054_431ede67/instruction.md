You are a forensics analyst recovering evidence from a compromised host. You have been assigned to analyze a suspicious binary left behind by an attacker. Intelligence suggests the malware bypassed local authentication mechanisms (resembling a JWT `alg=none` vulnerability) and communicates with a Command and Control (C2) server using an embedded TLS certificate and specific Content Security Policy (CSP) headers.

The suspicious binary is located at `/home/user/malware.elf`.

Your task is to write a Bash script at `/home/user/analyze_malware.sh` that automatically performs the following forensic steps when executed:

1. **ELF Analysis & TLS Extraction**: 
   The binary contains a custom ELF section named `.c2_cert`. Extract the raw contents of this section (which is a PEM-encoded X.509 certificate) and save it to `/home/user/extracted_cert.pem`.

2. **Certificate Parsing**:
   Parse the extracted certificate to obtain the `Issuer` and `Subject` strings. 
   Save these exact OpenSSL output lines (using `openssl x509 -noout -issuer -subject`) to `/home/user/cert_info.txt`.

3. **CSP Enforcement String Extraction**:
   The binary contains a hardcoded string used to inject Content Security Policy headers into local web views. The string starts with `JWT:alg=none|CSP:` and contains a `connect-src` directive.
   Extract the domain name specified in the `connect-src` directive of this CSP string (e.g., if the string is `...|CSP:default-src 'none';connect-src https://evil.local;...`, extract `https://evil.local`).
   Save ONLY the extracted C2 URL to `/home/user/c2_url.txt`.

Ensure your Bash script is executable and completely automates these steps. After writing the script, execute it to generate the three output files (`extracted_cert.pem`, `cert_info.txt`, and `c2_url.txt`).