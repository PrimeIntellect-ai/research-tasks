You are an application security engineer tasked with securing a vulnerable authentication infrastructure. The environment consists of three cooperating services shipped under `/app/`: Nginx, a Go Auth backend, and Redis.

**Part 1: Multi-Service Composition & mTLS Configuration**
The Go Auth service (runs on `127.0.0.1:8443`) requires mutual TLS (mTLS). Nginx (runs on `127.0.0.1:8080`) acts as a reverse proxy to the Go backend, but its configuration is currently broken because it lacks a valid client certificate to authenticate to the Go service. 

1. A Certificate Authority (CA) is provided at `/app/certs/ca.crt` and `/app/certs/ca.key`.
2. Generate a valid client certificate and private key for Nginx, signed by this CA. Place them at `/app/certs/client.crt` and `/app/certs/client.key`.
3. Update the Nginx configuration at `/app/nginx/nginx.conf` to proxy requests from `http://127.0.0.1:8080` to `https://127.0.0.1:8443`. You must configure Nginx to use the generated client certificate for upstream mTLS authentication.
4. The startup script `/app/start.sh` brings up Nginx, the Go backend, and Redis. You must ensure that running `curl http://127.0.0.1:8080/health` successfully returns HTTP 200 with the body `{"status": "ok"}`.

**Part 2: Token Vulnerability & Adversarial Classifier**
A penetration test revealed that attackers are exploiting the Auth service by sending encrypted JSON tokens containing SQL injection payloads in the `user` field. We have captured network traffic and isolated the encrypted payloads into two directories:
- `/app/corpus/clean/`: Contains files with legitimate encrypted tokens.
- `/app/corpus/evil/`: Contains files with malicious encrypted tokens.

Tokens are Base64-encoded. When decoded, the first 12 bytes are the AES-GCM nonce, and the rest is the ciphertext. The 32-byte AES key is stored in hex format at `/app/keys/aes.key`. Decrypted tokens are JSON objects of the form `{"user": "..."}`.

You must write a Go CLI program at `/app/classifier.go` that:
1. Takes a single Base64-encoded token as its first command-line argument (`os.Args[1]`).
2. Decrypts the token using the key from `/app/keys/aes.key`.
3. Parses the decrypted JSON.
4. Inspects the `user` field for SQL injection attempts. If the `user` field contains any of the following substrings (case-insensitive), it must be flagged as malicious: `union`, `select`, `drop`, `or 1=1`, `' --`.
5. Exits with code `0` if the payload is clean.
6. Exits with code `1` if the payload is malicious.

Build your Go program and place the executable at `/app/classifier`. The automated verifier will run your classifier against every file in the clean and evil corpora. It must achieve 100% accuracy (exit 0 for all clean, exit 1 for all evil) to pass.