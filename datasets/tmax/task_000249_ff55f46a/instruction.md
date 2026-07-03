You are a security engineer responding to a network breach. An attacker managed to compromise a management jump host and ran a packet sniffer. We have recovered a screen recording of the attacker's terminal during the breach, located at `/app/traffic_capture.mp4`. The video displays scrolling hex dumps and plaintext HTTP headers of traffic they intercepted.

Your mission involves three phases: Extrication, Auditing, and Credential Rotation.

**Phase 1: Extrication**
Analyze the video file `/app/traffic_capture.mp4`. The terminal output in the video contains intercepted HTTP traffic. You must use OCR or pattern matching on extracted frames to identify all leaked session cookies. The cookies follow the format `Set-Cookie: auth_session=[A-Za-z0-9]{16};`. 
Extract all unique `auth_session` values you can find in the video and save them to `/home/user/leaked_tokens.txt`, with one 16-character token per line. 

**Phase 2: Auditing**
Write a script located at `/home/user/audit_and_rotate.sh` (in the language of your choice) that reads the `leaked_tokens.txt` file. The script must scan localhost ports in the range 8080-8090. These ports host mock internal microservices over HTTPS.
For each open port, the script must test if the service is vulnerable by sending an HTTPS GET request to `/admin` with the leaked `auth_session` cookies. A vulnerable service will respond with an HTTP 200 OK for at least one of the leaked tokens. Ignore SSL certificate validation warnings during the scan.

**Phase 3: Credential Rotation**
For every vulnerable port identified in Phase 2, your script must automatically rotate the service's TLS credentials by generating a new set of keys and certificates. 
The script must generate a new self-signed X.509 certificate and private key with the following exact specifications:
- 2048-bit RSA key
- Valid for exactly 14 days
- Common Name (CN) set to `service.internal`
- Output paths: `/home/user/certs/port_<PORT>_key.pem` and `/home/user/certs/port_<PORT>_cert.pem` (where `<PORT>` is the vulnerable port number).

Ensure your script creates the `/home/user/certs/` directory if it does not exist. You may use `ffmpeg`, `tesseract-ocr`, `curl`, `openssl`, and any programming language available in the environment to accomplish this. You must run your pipeline so that `/home/user/leaked_tokens.txt` and the rotated certificates are successfully generated.