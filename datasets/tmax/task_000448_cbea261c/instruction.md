You are a forensics analyst investigating a compromised host. The attacker left behind a hidden data exfiltration pipeline consisting of a local firewall proxy, an Nginx reverse proxy, and a backend Python API. They used this pipeline to encrypt and serve sensitive system data. 

We need to recover the exfiltrated data by fixing and utilizing the attacker's own pipeline. The services are located in `/home/user/forensics_lab`.

Currently, the services are broken or misconfigured, preventing us from extracting the evidence. 
Here is the pipeline architecture:
`Client -> Firewall Proxy (Port 8000) -> Nginx Reverse Proxy (Port 8080) -> Backend Python API (Port 8081)`

Your task is to fix the pipeline so that the backend API can successfully serve the decrypted evidence.

1. **Firewall Proxy (`/home/user/forensics_lab/firewall.py`)**:
   The proxy listens on `127.0.0.1:8000` and forwards traffic to Nginx on port `8080`. 
   Currently, the proxy explicitly drops any requests containing the HTTP header `X-Forensics: true`. You must modify `firewall.py` to *allow* requests with this header to pass through to Nginx.

2. **Nginx Reverse Proxy (`/home/user/forensics_lab/nginx.conf`)**:
   Nginx listens on `127.0.0.1:8080` and forwards the `/evidence` endpoint to the backend API (`127.0.0.1:8081`). 
   However, the attacker misconfigured it to strip out all cookies before forwarding. Modify `nginx.conf` to ensure the `Cookie` header is passed seamlessly to the upstream backend.

3. **Decryption Script (`/home/user/forensics_lab/decrypt.sh`)**:
   The backend API expects a cookie named `Auth-Token=admin_access`. When received, it invokes a Bash script at `./decrypt.sh`.
   The `decrypt.sh` script is incomplete. You must write the Bash command inside `decrypt.sh` to decrypt the file `/home/user/forensics_lab/evidence.enc`. 
   - The file was encrypted using `openssl` with the `aes-256-cbc` cipher and `-pbkdf2`.
   - The passphrase is: `f0r3ns1cs!`
   - The script must output the decrypted plaintext to `STDOUT`.

Once you have made the necessary fixes, ensure all services are running. You can restart them using `/home/user/forensics_lab/start_services.sh`. Leave the services running on their respective ports so our automated verification system can test the endpoint.