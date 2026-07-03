You are a network security engineer investigating a recent breach. Our monitoring systems captured a video recording of an attacker's terminal dashboard, which is stored at `/app/dashboard_capture.mp4`. 

We believe the video contains a brief visual flash (only a few frames) showing an analysis of a malicious ELF binary. In that specific frame, the dashboard displays the attacker's command and control (C2) server IP, port, and a specific TLS certificate subject name they expect to connect to.

Your task has two parts:

Part 1: Video Forensics
Analyze the video file at `/app/dashboard_capture.mp4` to extract the hidden frame containing the ELF analysis. From that frame, determine:
- The target listening Port.
- The expected TLS Certificate Common Name (CN).
- A specific 16-byte hex payload that the C2 server uses as an initial knock.

Write these extracted values to `/home/user/extracted_intel.json` in the following format:
```json
{
  "port": 12345,
  "tls_cn": "example.com",
  "knock_payload": "0123456789abcdef0123456789abcdef"
}
```

Part 2: Active Interception (Rust)
Using Rust, write a multi-protocol honeypot service located at `/home/user/honeypot`. The service must:
1. Generate a self-signed TLS certificate locally using the Common Name (CN) extracted from the video.
2. Bind and listen on the specific port extracted from the video on `0.0.0.0`.
3. Accept incoming connections. It must support both Raw TCP (for the knock) and HTTPS.
4. When a connection is established:
   - If the incoming data matches the exact 16-byte hex `knock_payload` (sent as raw bytes, not an ascii string), the server must respond with the ASCII string `ACK_KNOCK` and close the connection.
   - If the incoming connection is an HTTPS request to the path `/submit_elf`, it must return an HTTP 200 OK with the body `SUBMISSION_ACCEPTED`.
5. Ensure the Rust service is compiled and actively running in the background. Do not stop the service once started, as our automated systems will immediately attempt to connect to it.

You may use any Rust crates you need (e.g., `tokio`, `rustls`, `hyper`, `rcgen`).