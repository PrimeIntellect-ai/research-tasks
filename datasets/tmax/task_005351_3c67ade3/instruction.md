You are an infrastructure engineer stepping into a partially automated provisioning environment. A previous engineer left the company abruptly, and their Docker-based configuration was lost. However, they left an automated voicemail system recording that dictates the backend security pin, which corresponds to the internal network port assigned to the mail routing service.

Your task consists of the following phases:

1. **Configuration Recovery (Audio Processing):**
   There is an audio file located at `/app/voicemail.wav`. It contains a sequence of DTMF (Dual-Tone Multi-Frequency) tones. You must decode these tones to recover a 4-digit number. This number is the `BACKEND_PORT`. 
   *(Hint: You can use tools like `sox`, `multimon-ng`, or write a short Python script using standard libraries to decode the audio).*
   Once decoded, ensure this value is exported as `BACKEND_PORT` in `/home/user/.bash_profile`.

2. **Backend Service Implementation:**
   Write a lightweight backend service (in Python, Node.js, or via advanced bash scripting) that acts as an SMTP sinkhole. It must:
   - Listen on `127.0.0.1` at the port dictated by `BACKEND_PORT`.
   - Accept standard unauthenticated SMTP connections.
   - For any message received, append the sender, recipient, and message body to `/home/user/mail_sink.log`.

3. **Frontend & Health Check Configuration:**
   The external load balancer expects two frontend interfaces:
   - **SMTP Proxy (Port 2525):** Listen on `0.0.0.0:2525` and transparently route all TCP traffic to your backend SMTP service on `127.0.0.1:$BACKEND_PORT`.
   - **Health Monitor (Port 8080):** Listen on `0.0.0.0:8080`. When an HTTP GET request is made to `/health`, it must return an HTTP 200 OK status with the exact JSON payload: `{"status": "healthy", "backend_port": <YOUR_DECODED_PORT>}`.

4. **Process Management:**
   Since you do not have root access or `systemd`, you must create a custom service lifecycle manager script at `/home/user/start_services.sh`. This script must:
   - Start the backend, frontend proxy, and health check services in the background.
   - Save the Process IDs (PIDs) of these services into `/home/user/run/backend.pid`, `/home/user/run/proxy.pid`, and `/home/user/run/health.pid` respectively.
   - Be executable (`chmod +x`).

Execute the necessary commands to decode the audio, write the service scripts, and run your `start_services.sh` script to leave the system in the desired running state.