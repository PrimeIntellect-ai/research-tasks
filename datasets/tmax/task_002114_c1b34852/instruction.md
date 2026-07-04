As a forensics analyst investigating a compromised Linux host, you have discovered a suspicious, stripped binary left behind by the attackers at `/app/vault_server`. This binary appears to be a custom HTTPS server used to temporarily stash exfiltrated evidence before it is shipped off-network.

You need to write a fully automated Bash script at `/home/user/recover.sh` to extract the stashed evidence. 

Through preliminary reverse engineering, you know the following about `/app/vault_server`:
1. It is an HTTPS-only server that requires a TLS certificate and private key to start.
2. It accepts command-line arguments: `/app/vault_server --cert <path_to_cert> --key <path_to_key> --port <port>`
3. It exposes a protected endpoint at `GET /api/v1/evidence?chunk=<id>` (where `<id>` is an integer from 1 to 500).
4. The endpoint is protected by JWT authentication via the `Authorization: Bearer <token>` header.
5. The JWT implementation is flawed: it is vulnerable to the "algorithm none" attack. It will grant access if it receives an un-signed JWT (header `{"alg":"none","typ":"JWT"}`) as long as the payload contains `{"access_level":"system"}`.

Your script (`/home/user/recover.sh`) must perform the following actions:
1. **TLS Certificate Management:** Generate a temporary self-signed RSA-2048 certificate (`cert.pem`) and key (`key.pem`) in `/home/user/`.
2. **Service Setup:** Launch `/app/vault_server` in the background on port `8443` using the generated certificate. Give it a few seconds to initialize.
3. **Exploit Crafting:** Construct the malicious `alg: none` JWT entirely using Bash utilities (remember to use valid base64url encoding without padding).
4. **Data Recovery:** Loop through chunk IDs 1 to 500. Use `curl` to send the crafted JWT to the server and retrieve each chunk. 
5. **Output & Access Control:** Append all successfully retrieved raw response bodies to `/home/user/recovered.log`. Once finished, securely set the permissions of `/home/user/recovered.log` to `600` (read/write for owner only).

Ensure your script is self-contained, handles the base64url encoding correctly (replacing `+` with `-`, `/` with `_`, and stripping `=` padding), and suppresses unnecessary `curl` output so the script runs cleanly.