As an incident responder, you are investigating a recent breach. We have a screen recording of the attacker's terminal session captured during the incident, located at `/app/incident_screen.mp4`. We need you to reverse-engineer the attacker's access and set up a secure honeypot service to monitor further attempts.

Your tasks are:

1. **Video Analysis & Credential Recovery**:
   Extract the frames from `/app/incident_screen.mp4`. At some point in the video, the attacker accidentally echoes a partial password to the screen before clearing it. The password format is `Secure_XXXX`, where `XXXX` is a 4-digit number. The video reveals the first two digits. You must identify these two digits from the video frames. Then, you must write a C program to brute-force the remaining two digits against an intercepted SHA-256 hash left by the attacker in `/home/user/intercepted.hash`. Write the fully cracked password to `/home/user/cracked_password.txt`.

2. **TLS/SSL Setup**:
   Generate a self-signed TLS certificate (`server.crt`) and private key (`server.key`) in `/home/user/certs/`. The certificate must have the Common Name `honeypot.local`.

3. **Secure Honeypot Service in C**:
   Write a C program at `/home/user/honeypot.c` and compile it to `/home/user/honeypot`. This program must:
   - Act as an HTTPS server listening on `127.0.0.1:8443`.
   - Use OpenSSL to load the certificate and key from `/home/user/certs/`.
   - Implement process isolation: immediately after binding to the port, the program must chroot to `/home/user/jail` and drop privileges to the `nobody` user (UID 65534). (Ensure the jail directory exists and the certs are accessible or loaded before chrooting).
   - Read incoming HTTP GET requests.
   - Inspect the HTTP headers for a specific cookie: `Cookie: AuthToken=<cracked_password>`, where `<cracked_password>` is the exact password you recovered.
   - If the cookie is present and exactly matches the cracked password, respond with an HTTP 200 OK and the body `ACCESS GRANTED`.
   - If the cookie is missing or incorrect, respond with an HTTP 403 Forbidden and close the connection.

Ensure the service is running in the background when you complete your task.