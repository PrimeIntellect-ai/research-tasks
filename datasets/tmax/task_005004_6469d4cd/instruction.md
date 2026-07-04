You are a network engineer investigating a recent server compromise. You have captured network logs and a recovered video file showing the attacker's screencast. Your goal is to analyze these artifacts, extract the attacker's credentials, and set up a hardened SSH honeypot alongside an HTTP reporting service.

Here are your objectives:

1. **Log Analysis**: Parse the security log located at `/home/user/auth.log`. Identify the IP address of the attacker who successfully logged in via brute-force. A successful login is indicated by the string "Accepted password". Write the attacker's IP to `/home/user/attacker_ip.txt`.

2. **Video Analysis**: We recovered a screencast of the attacker's session at `/app/attacker_screencast.mp4`. The attacker accidentally reveals their backdoor password in plaintext on the terminal screen at exactly the 3-second mark (00:00:03). Extract this frame (using `ffmpeg` and `tesseract` or manual inspection via console tools if needed, or you can read it directly if you process the image) and find the password. The password follows the format `B@ckD00r_...`. Write this password to `/home/user/attacker_password.txt`.

3. **Hardened SSH Honeypot**: Set up a user-space SSH daemon (`sshd`) listening on `127.0.0.1:8022`. 
   - You must write a custom `sshd_config` file at `/home/user/sshd_config`.
   - The SSH server must run as the current user (`user`).
   - It must accept connections using the password you found in the video. (You may need to set the password for a dummy local user or use a PAM module/script, but since you don't have root, you should configure `sshd` to use a fake authentication script or just rely on the `user` account if you can change its password. Alternatively, use a Python SSH server like `paramiko` to emulate an SSH server that ONLY accepts the username `admin` and the password from the video). Let's use a Python SSH honeypot script since configuring `sshd` without root for password auth can be tricky. Write a Python or Bash-based SSH server listening on `127.0.0.1:8022` that accepts username `admin` and the exact password from the video.

4. **HTTP Reporting Service**: Create a JSON report at `/home/user/report.json` with the following exact format:
   ```json
   {
     "attacker_ip": "<IP_FOUND_IN_LOG>",
     "backdoor_password": "<PASSWORD_FOUND_IN_VIDEO>"
   }
   ```
   Serve this file via an HTTP server listening on `127.0.0.1:8080`. The verifier will make a GET request to `http://127.0.0.1:8080/report.json`.

**Final State**:
- Your SSH honeypot must be actively running and listening on `127.0.0.1:8022`.
- Your HTTP server must be actively running and listening on `127.0.0.1:8080`.
- Both servers must remain running in the background.

Use Bash as your primary tool for scripting the log parsing and service launching.