You are an incident responder analyzing a recent server breach. We have collected artifacts from the compromised machine. Your goal is to extract evidence, correlate logs, and deploy a secure mitigation webhook written entirely in Bash.

**Step 1: Video Artifact Analysis**
We intercepted an encoded video file left by the attacker at `/app/evidence.mp4`. The attacker carelessly embedded their command-and-control HMAC secret key in the subtitle stream of this video file. 
Use `ffmpeg` or `ffprobe` to extract the subtitle stream and find the secret key. The subtitle text contains the string `C2_SECRET: <the_secret>`. Extract this secret.

**Step 2: Privilege Escalation Auditing**
The attacker left several binaries in `/home/user/suspicious/`. Analyze this directory to find the privilege escalation vector. Specifically, identify the single executable file that has the SUID bit set. Compute the SHA256 hash of this binary.

**Step 3: Security Log Parsing**
Analyze the web server log at `/home/user/access.log`. The attacker injected a custom HTTP header `X-Exploit-Payload` during their initial breach. Find the IP address of the attacker who sent the request containing this header.

**Step 4: Deploy the Responder Webhook (Multi-Protocol)**
You must write a Bash script `/home/user/webhook.sh` and run it in the background. This script must act as an HTTP server listening on TCP port `127.0.0.1:8080` using `socat` or `nc` (socat is highly recommended for handling HTTP correctly in bash).

The service must implement the following specification:
1. Accept HTTP GET requests to `/audit`.
2. Inspect the incoming request for the `X-Incident-Auth` header.
3. Validate the token provided in the header. The valid token is an HMAC-SHA256 signature of the attacker's IP address (from Step 3), signed using the `C2_SECRET` (from Step 1). The expected token format in the header is the hex representation of the HMAC.
   *(Hint: you can compute this in bash using `echo -n "<ip>" | openssl dgst -sha256 -hmac "<secret>"`)*
4. If the token is missing or invalid, the server must respond with exactly:
   `HTTP/1.1 403 Forbidden\r\n\r\n`
5. If the token is valid, the server must respond with exactly:
   `HTTP/1.1 200 OK\r\n\r\n<SHA256_HASH>`
   where `<SHA256_HASH>` is the hash of the SUID binary you found in Step 2.

**Execution**
Ensure your webhook service is running continuously and listening on `127.0.0.1:8080` before you finish the task. Do not use Python, Node, or Go for the webhook; it must be implemented via Bash (helper tools like awk, grep, openssl, and socat are allowed).