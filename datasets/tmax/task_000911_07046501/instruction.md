You are a Linux systems engineer responsible for hardening and configuring a secure email relay and connectivity service. We have transitioned to a new architecture where inbound messages must be routed through secure SSH tunnels to specific backend processing ports, based on the sender's user group.

Your task involves setting up the port forwarding, parsing the configuration, and implementing the relay router.

Here are the requirements:
1. **Extract Architecture Configuration**: There is an architecture diagram located at `/app/architecture.png`. You must use `tesseract` to extract the text from this image. It contains the "Access Control Lists (ACL)" defining which users belong to which groups, and the "Tunnel Mappings" defining which target backend port each group's traffic should be routed to via SSH tunneling.
2. **Establish SSH Tunnels**: Using the existing SSH key at `/home/user/.ssh/id_rsa`, set up background SSH local port forwarding to the local unprivileged SSH daemon running on port `2222` (`user@127.0.0.1`). 
   - You must map local port `8001` to the backend port specified for the `Admins` group in the image.
   - You must map local port `8002` to the backend port specified for the `Devs` group in the image.
3. **Implement the Relay Service**: Write a Python or Bash script at `/home/user/mail_router.py` (or `.sh`) that listens on `stdin` for a JSON-formatted email message, evaluates the sender against the extracted ACLs, and forwards the raw JSON payload via TCP socket to the corresponding forwarded local port (`8001` for Admins, `8002` for Devs).
   - Expected input format on stdin: `{"sender": "alice", "body": "system alert"}`
   - If the sender is in the `Admins` group, send the exact JSON string to `127.0.0.1:8001`.
   - If the sender is in the `Devs` group, send the exact JSON string to `127.0.0.1:8002`.
   - If the sender is not recognized, drop the message and exit with code 1.
   - Ensure the script reads a single line of JSON, sends it, closes the connection, and exits with code 0 on success.

Ensure your SSH tunnels remain active in the background. Do not require root privileges (`sudo`). We will run an automated metric-based verifier that pumps 100 randomly generated emails through your `/home/user/mail_router.py` script and measures the successful delivery rate to the backend mock servers. You must achieve a delivery accuracy of 1.0 (100%).