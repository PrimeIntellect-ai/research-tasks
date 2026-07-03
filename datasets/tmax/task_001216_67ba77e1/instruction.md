You are an incident responder investigating a series of attacks on our internal API. The attacker is exploiting a cryptographic vulnerability (AES-ECB mode predictability) in our session handling, causing backend services to crash.

Your task has two parts:

**Part 1: Build a malicious payload detector**
We have captured samples of normal and malicious HTTP session cookies. Malicious cookies contain cryptographically repeating 16-byte blocks (a hallmark of AES-ECB mode manipulation) when base64-decoded. 

Write a Bash script at `/home/user/detect.sh` that takes a single file path as an argument. The file contains exactly one base64-encoded session string. Your script must:
1. Read the base64 string from the file.
2. Decode it into binary.
3. Convert the binary to a hex string.
4. Analyze the hex string to detect if *any* 16-byte block (32 consecutive hex characters) is repeated anywhere else in the decoded payload.
5. Exit with code `1` (reject) if a repeated block is found (malicious).
6. Exit with code `0` (accept) if no blocks are repeated (clean).

*Hint: Standard utilities like `base64`, `xxd`, `fold`, `sort`, and `uniq` are available and perfect for this.*

**Part 2: Reconfigure the service pipeline**
We have a multi-service stack that needs to be brought online with strict sandboxing and isolation.
- An Nginx reverse proxy using the configuration file at `/home/user/nginx/nginx.conf`.
- A Python backend API running on `127.0.0.1:9000`.

Currently, Nginx is misconfigured. Edit `/home/user/nginx/nginx.conf` so that:
1. It listens on port `8080`.
2. It proxies all traffic for `/api/` to `http://127.0.0.1:9000`.
3. It drops all requests containing the HTTP header `X-Debug-Bypass: true` by returning a 403 Forbidden.

Once configured, start Nginx in the background using your custom configuration: `nginx -c /home/user/nginx/nginx.conf`. 

Ensure your script `/home/user/detect.sh` is executable. You do not need to integrate `detect.sh` directly into Nginx; the automated verification suite will test it independently against our offline corpora of evil and clean payloads, and will independently send HTTP requests to port 8080 to verify your Nginx routing and header filtering.