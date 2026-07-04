You are acting as a penetration tester analyzing a leaked screen recording of a server administrator's session. The video file is located at `/app/admin_session.mp4`. 

During the recording, the administrator briefly flashes several QR codes on the screen. These QR codes contain a mix of encrypted SSH credentials and various login URLs. We suspect that some of these login URLs are vulnerable to open redirects.

Your task is to create a robust Bash script at `/home/user/analyze.sh` that automates the following pipeline:
1. **Frame Extraction**: Extract frames from the `/app/admin_session.mp4` video using `ffmpeg`.
2. **Data Recovery**: Scan the extracted frames for QR codes using `zbarimg` and extract their raw text payloads.
3. **Decryption**: Some payloads are AES-256-CBC encrypted strings (Base64 encoded) prefixed with `ENC:`. The symmetric key is hardcoded as `Sup3rS3cr3tP4ssw0rd!` and the IV is `1234567890123456`. Decrypt these strings using OpenSSL.
4. **Vulnerability Scanning**: Other payloads are URLs. You must analyze these URLs and identify those that contain an open redirect vulnerability in their login flow (e.g., URLs where a `redirect_uri` or `next` parameter points to an external, untrusted domain like `http://evil.com` or `https://attacker.net`).
5. **Output Generation**: Your script must output exactly two files:
   - `/home/user/decrypted_keys.txt`: A plain text file containing one decrypted SSH credential per line.
   - `/home/user/open_redirects.txt`: A plain text file containing only the URLs (one per line) that are confirmed to be vulnerable to open redirects based on the parameter analysis.

Your script must be fully automated, taking a video file path as its first argument (e.g., `./analyze.sh /app/admin_session.mp4`), so that it can be evaluated against a separate held-out test video. Ensure your bash script is executable. You may use standard tools like `ffmpeg`, `zbarimg`, `openssl`, `grep`, `awk`, and `sed`.