You are a security auditor investigating a compromised system. The incident response team has recovered an intercepted audio transmission at `/app/intercepted.wav` and a suspicious compiled binary at `/app/validator.elf`. 

Your objective is to analyze these artifacts and construct a honeypot service to trap the attackers using their own backdoor authentication flow.

Step 1: Audio Analysis
Listen to or transcribe the audio file at `/app/intercepted.wav`. It contains a spoken override passcode (e.g., "the passcode is alpha seven seven"). Extract this passcode, convert it to lowercase, and remove any spaces (e.g., `alpha77`).

Step 2: Reverse Engineering
Analyze the `/app/validator.elf` binary. It is a simple validation tool used by the attackers. Determine:
- The custom HTTP Header name it expects for backdoor authentication.
- The specific HTTP Cookie name it verifies.

Step 3: Honeypot Deployment
Write and execute a multi-language or Python-based honeypot that implements the following multi-protocol services:

Service A (HTTP) on `127.0.0.1:8080`:
- Must respond to `GET /admin_check`.
- Must validate that the custom HTTP Header (found in Step 2) exactly matches the passcode extracted in Step 1.
- Must validate that the HTTP Cookie (found in Step 2) is present in the request (its value can be anything).
- If both the header and cookie are valid, return an HTTP 200 OK with the exact JSON body: `{"access": "granted"}`
- If either is missing or invalid, return an HTTP 403 Forbidden.

Service B (Raw TCP) on `127.0.0.1:8081`:
- Must act as a heartbeat monitor. 
- When it receives the exact string `PING\n`, it must respond with `PONG\n` and keep the connection open or close it gracefully.

Run your honeypot service in the background so that it is actively listening on both ports when you finish the task.