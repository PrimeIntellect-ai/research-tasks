You are a network security engineer tasked with securing a legacy authentication service that is vulnerable to open redirect attacks.

We have intercepted a voicemail from the system administrator containing emergency access credentials and configuration details. This audio file is located at `/app/voicemail.wav`.

You must write and run a secure reverse proxy in Go that sits in front of the legacy backend. Your proxy must implement authentication, patch the open redirect vulnerability, and securely connect to the backend.

Here are your requirements:
1. **Listen Address**: Your Go proxy must listen for incoming HTTP traffic on `127.0.0.1:9090`.
2. **Upstream Backend**: The legacy backend is running at `https://127.0.0.1:8443`. Your proxy must forward valid requests to this backend.
3. **Certificate Chain Validation**: The backend uses a custom internal CA. You must configure your Go proxy's HTTP client to validate the upstream server's TLS certificate using the CA certificate provided at `/app/ca.crt`. Do NOT use `InsecureSkipVerify: true`.
4. **Authentication**: Extract the secret 5-digit emergency token spoken in `/app/voicemail.wav`. Your proxy must inspect the `Authorization` header of all incoming requests (format: `Bearer <token>`). If the token is missing or incorrect, return an HTTP 401 Unauthorized status.
5. **Open Redirect Protection**: The backend login flow uses a `next` query parameter (e.g., `/?next=/dashboard`). Extract the allowed internal domain spoken in the voicemail. Your proxy must inspect the `next` parameter:
   - If `next` is a relative path (e.g., `/settings`), allow it.
   - If `next` is an absolute URL, its host MUST exactly match the allowed internal domain.
   - If `next` points to any other domain (e.g., `http://evil.com/` or `//attacker.com`), your proxy must intercept the request and return an HTTP 403 Forbidden status without forwarding it.

Write your code in `/home/user/secure_proxy.go`, compile it, and run it in the background so that it is listening on port 9090. Leave it running for the automated verification system to test. You may use any tools (like `ffmpeg` or `whisper`) to transcribe the audio file.