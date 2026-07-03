You are a DevSecOps engineer tasked with enforcing policy as code for an internal infrastructure team. The team currently relies on a proprietary, legacy certificate generation utility to provision TLS certificates for internal microservices. This utility is located at `/app/legacy_cert_gen`. It is a stripped ELF binary, and we suspect it occasionally generates certificates that violate our modern cryptographic policies (e.g., using deprecated signature algorithms like MD5 or SHA1, or generating RSA keys smaller than 2048 bits).

Your task is to create a robust Bash script at `/home/user/policy_enforcer.sh` that acts as a secure wrapper and validator. 

Requirements for `/home/user/policy_enforcer.sh`:
1. The script must accept a single argument: a domain name (e.g., `service.internal`).
2. It must execute the `/app/legacy_cert_gen` binary securely. Since the binary is untrusted and legacy, your bash script must execute it with restricted privileges (e.g., utilizing `bwrap`, `chroot`, or strict `ulimit` isolation) to prevent it from reading outside its working directory or opening network connections. The binary takes the domain as its only argument and writes `cert.pem` and `key.pem` to the current working directory.
3. After generation, your script must parse the resulting `cert.pem` using `openssl`.
4. It must enforce the following strict cryptographic policies on the generated certificate:
   - The public key must be an RSA key of at least 2048 bits.
   - The signature algorithm must be exactly `sha256WithRSAEncryption` or `sha512WithRSAEncryption` (no SHA1, MD5, etc.).
   - The certificate must be valid for at least 30 days but no more than 397 days.
5. If the certificate passes all policy checks, the script should print `PASS: <domain>` to stdout and exit with code 0.
6. If the certificate fails any policy check or the binary crashes, the script should securely delete the generated `.pem` files, print `FAIL: <domain>` to stdout, and exit with code 1.

You will need to analyze the binary format of the ELF executable to ensure you provide it the correct isolated environment (e.g., identifying required shared libraries). Ensure your Bash script is highly optimized, as it will be run thousands of times in a pipeline.