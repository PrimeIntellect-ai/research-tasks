You are a deployment engineer tasked with rolling out a local deployment pipeline and an audio-processing microservice. Because you do not have root access, all services must run under your user account (`/home/user/`) and use unprivileged ports.

Your objective is to complete the following four integrations:

1. **SMTP Mailing List Server**
Create and run a custom SMTP server listening on `127.0.0.1:2525`. This service must accept all incoming emails and append the raw email content (headers and body) to `/home/user/maillog.txt`. It should gracefully handle standard SMTP commands (HELO/EHLO, MAIL FROM, RCPT TO, DATA, QUIT). Keep this service running in the background.

2. **Git Deployment Hook**
Initialize a bare Git repository at `/home/user/deploy.git`. 
Configure a `post-receive` hook in this repository that does two things whenever new code is pushed:
a) Checks out the newly pushed code into a working tree at `/home/user/app_code` (create this directory).
b) Connects to the local SMTP server at `127.0.0.1:2525` and sends an email to `admin@localhost` with the exact subject `Subject: Code Pushed` to notify the mailing list.
c) Appends a deployment log entry to `/home/user/logs/deploy.log`.

3. **Audio Transcription Web Service**
We have received a voicemail recording related to the deployment, located at `/app/voicemail.wav`.
Write and start an HTTP web service listening on `127.0.0.1:8080`. 
When the service receives a GET request to `/transcript`, it must read `/app/voicemail.wav`, transcribe the spoken English audio to text, and return the transcription as plain text in the HTTP response body.
Additionally, this web service must log every incoming request by appending a line to `/home/user/logs/access.log`. Keep this service running in the background.

4. **Log Rotation Configuration**
To manage the logs created by the above services, create a logrotate configuration file exactly at `/home/user/logrotate.conf`. 
This file must be configured to manage all logs in `/home/user/logs/*.log` with the following rules:
- Rotate daily.
- Keep exactly 5 compressed backups.
- Missing log files should not produce an error.
- Do not use `su` directives (as you do not have root privileges).

You may use any programming language or scripting tools available (or installable via user-level package managers like `pip`) to implement these services. Ensure that both the SMTP server on port 2525 and the HTTP server on port 8080 are actively running and bound to the loopback interface before you finish the task.