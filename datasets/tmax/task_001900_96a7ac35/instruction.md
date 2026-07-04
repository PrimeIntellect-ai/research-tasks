You are a DevSecOps engineer implementing a policy-as-code verification step for a CI/CD pipeline. Your team embeds cryptographic trust and authentication claims directly inside compiled binaries.

You need to write a Python script at `/home/user/check_binary.py` that takes exactly one command-line argument: the path to an ELF binary file. The script must perform the following policy checks:

1. **Binary Analysis**: Extract two custom sections from the provided ELF binary:
   - `.cert_chain`: Contains a PEM-encoded X.509 certificate chain (ordered: Leaf, then Root CA).
   - `.auth_token`: Contains a JWT (JSON Web Token) representing the binary's deployment authorization.

2. **Certificate Chain Validation**: 
   - Parse the certificates from the `.cert_chain` section.
   - Verify that the Leaf certificate is cryptographically signed by the Root CA.
   - Verify that the Root CA is self-signed.
   *(Note: You do not need to check expiration dates for this exercise, just cryptographic signatures).*

3. **Authentication Flow Testing**:
   - Extract the public key from the Leaf certificate.
   - Use this public key to verify the signature of the JWT found in the `.auth_token` section.
   - Extract the `sub` (subject) claim from the verified JWT payload.

4. **Output Generation**:
   After processing the binary, your script must output a JSON file at `/home/user/result.json` with the following precise schema:
   ```json
   {
     "elf_valid": true,
     "chain_valid": true,
     "jwt_valid": true,
     "jwt_subject": "<the extracted sub claim>"
   }
   ```
   If any check fails, the respective boolean should be `false`, and `jwt_subject` should be `null`. 

For testing, an example binary has been placed at `/home/user/target_binary.elf`. 
You can use standard CLI tools (like `objcopy` or `readelf`) invoked from Python via `subprocess`, or Python libraries if they are available in your environment. The standard python packages `cryptography` and `PyJWT` are available.