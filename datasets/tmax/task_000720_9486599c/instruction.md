You are an edge computing engineer managing an IoT device deployment. The device processes voice commands and routes them to a local backend, but we are facing two critical issues: a network misconfiguration in our containerized stack, and a lack of input sanitization for malicious override commands.

Your objectives:

1. **Connectivity Diagnostics & Service Lifecycle:**
   There is a Docker Compose stack located at `/home/user/edge-stack/docker-compose.yml`. It runs two services: `api` and `worker`. Currently, the `worker` service cannot reach the `api` service due to a network isolation misconfiguration. 
   - Modify the `docker-compose.yml` so both services reside on the same custom bridge network (name it `edge_net`).
   - Start the stack in detached mode. Ensure both services are running and `worker` can successfully resolve and ping `api`.

2. **Audio Transcription & Adversarial Filtering:**
   Our IoT devices are vulnerable to a specific spoken override command. We have captured an isolated recording of this malicious command at `/app/override_command.wav`.
   - Transcribe the audio file to identify the exact secret override phrase.
   - Write a standalone Python script at `/home/user/sanitize.py` that acts as a command sanitizer.
   - The script must accept exactly one CLI argument: the path to a text file containing a transcribed command.
   - The script must read the file and check for the presence of the secret override phrase (case-insensitive).
   - If the phrase is present, the file is malicious: exit with status code `1`.
   - If the phrase is NOT present, the file is safe: exit with status code `0`.

Ensure your script is executable (`chmod +x /home/user/sanitize.py`) and begins with an appropriate shebang. Automated tests will verify your Docker Compose configuration and validate your sanitizer script against a large corpus of safe and malicious transcripts.