You are an observability engineer tasked with updating a custom dashboard backend to expose a recent audio incident report. 

We have received an audio file at `/app/incident_report.wav` which contains a spoken description of a recent incident. 

Your task involves writing a C-based backend service, creating a configuration file, and setting up a minimal deployment script that mimics a staged rolling deployment with backup and restore capabilities.

Step 1: Audio Processing
Analyze the audio file `/app/incident_report.wav` and transcribe the spoken incident description. You may install and use any transcription tools available in the standard repositories (e.g., Python's SpeechRecognition with pocketsphinx, or whisper if you prefer to install it). Save the exact transcribed text to `/home/user/incident_text.txt`.

Step 2: Configuration Management
Create a configuration file at `/home/user/backend.conf` with the following key-value pairs (one per line):
HTTP_PORT=8080
TCP_PORT=8081
INCIDENT_FILE=/home/user/incident_text.txt

Step 3: C Dashboard Backend
Write a C program at `/home/user/dashboard_backend.c` that acts as our new telemetry service.
The program must:
1. Parse `/home/user/backend.conf` to read the ports and incident file path.
2. Read the contents of the incident file.
3. Start a multi-protocol server listening on both ports:
   - On the `HTTP_PORT` (8080), it must accept HTTP GET requests and respond with a valid `200 OK` HTTP response, where the body is a JSON object: `{"incident": "<transcribed_text>"}`.
   - On the `TCP_PORT` (8081), it must accept raw TCP connections, send the `<transcribed_text>` followed by a newline (`\n`), and immediately close the connection.
You may use standard POSIX sockets and threads or `fork()` to handle concurrent connections or simply handle them in a non-blocking loop.

Step 4: Deployment Pipeline
Write a bash script at `/home/user/deploy.sh` that implements a deployment strategy:
1. Ensure a backup directory exists at `/home/user/backups/`.
2. If an existing `backend.bin` is running, back it up to `/home/user/backups/backend_<timestamp>.bin`.
3. Compile `/home/user/dashboard_backend.c` to `/home/user/backend.bin`. If compilation fails, the script should exit and NOT stop the currently running service.
4. If compilation succeeds, gracefully terminate the old `backend.bin` process.
5. Start the new `/home/user/backend.bin` process in the background, redirecting its output to `/home/user/backend.log`.

Step 5: Execution
Run your `deploy.sh` script to deploy the backend. Ensure the C service is running and actively listening on both ports before completing the task.