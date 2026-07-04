You are a penetration tester analyzing an intercepted data leak. We have recovered a voicemail recording at `/app/voicemail.wav`.

Your task is to:
1. Transcribe the audio file to understand the required vulnerability mitigation and the specific task instructions.
2. Calculate the cryptographic SHA-256 hash of the `/app/voicemail.wav` file.
3. Bring up an HTTP web server listening on `127.0.0.1:8080`.
4. When an HTTP GET request is made to `/`, the server must return a `200 OK` response.
5. To mitigate the specific CWE (vulnerability) mentioned in the audio, the HTTP response MUST include a strict `Content-Security-Policy` header explicitly setting `default-src 'none'`.
6. The body of the HTTP response must contain the exact SHA-256 hash of the `.wav` file (just the hex string, no filename).

You may use Bash, `socat`, `nc`, or standard Python modules to run the server, but it must run continuously in the background so it can be verified. Keep the server running once configured.