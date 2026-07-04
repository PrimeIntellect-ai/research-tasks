You are a DevSecOps engineer tasked with securing a microservice's authentication layer. The current system is vulnerable to a JWT "algorithm confusion / none algorithm" attack, has unsecured cryptographic material, and lacks strict network policies.

Perform the following tasks to enforce security policies as code:

1. **Cryptographic Setup & File Permissions**:
   - Create a directory `/home/user/app/keys`.
   - Generate a self-signed Root CA certificate (`ca.crt`) and private key (`ca.key`).
   - Generate a leaf certificate (`server.crt`) and private key (`server.key`) signed by the Root CA.
   - All keys must be RSA 2048-bit.
   - Enforce strict access control: The `/home/user/app/keys/server.key` file MUST have exactly `400` permissions.

2. **Secure Token Validation (Python)**:
   - Write a Python script at `/home/user/app/validate_jwt.py`.
   - The script must read a JWT string from standard input.
   - It must validate the JWT using the PyJWT library, extracting the public key from `/home/user/app/keys/server.crt`.
   - **Crucial:** It must explicitly reject tokens with `algorithm="none"` or symmetric algorithms (like HS256) when an RSA key is expected. It should only accept `RS256`.
   - The script must print exactly `VALID` to standard output if the token is valid and correctly signed, and exactly `INVALID` if it fails validation or has a malicious algorithm.

3. **Network Policy Configuration**:
   - Although you do not have root access to apply firewall rules, write a shell script at `/home/user/app/firewall.sh` representing the desired state.
   - The script must contain exact `iptables` commands to:
     1. Append a rule to the INPUT chain to ACCEPT incoming TCP traffic on port 8000 from `127.0.0.1`.
     2. Append a rule to the INPUT chain to DROP incoming TCP traffic on port 8000 from any other IP address.

Ensure all dependencies (like `PyJWT` and `cryptography`) are installed in the user environment if you need to test your script.