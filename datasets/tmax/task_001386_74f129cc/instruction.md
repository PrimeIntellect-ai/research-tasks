You are a deployment engineer tasked with rolling out an update to our internal mailing list server. However, the exact configuration parameters for this deployment were left in a voicemail by the lead architect.

Your tasks are:
1. **Audio Transcription**: 
   An audio file of the voicemail is located at `/app/voicemail.wav`. Transcribe this audio file and save the exact text to `/home/user/transcript.txt`. You may install any tools you need (like `ffmpeg` or build tools) to process or transcribe the audio. The accuracy of your transcription is critical and will be graded programmatically.

2. **Health Check Implementation in C**:
   The voicemail mentions a specific port number and a timeout threshold for the new mailing list service. 
   Write a C program at `/home/user/health_monitor.c` that:
   - Takes two command-line arguments: `<port>` and `<timeout_seconds>`.
   - Attempts a TCP connection to `127.0.0.1` on the specified port.
   - If the connection is successful within the timeout, it should print "HEALTHY" and exit with code 0.
   - If it fails or times out, it should print "UNHEALTHY" and exit with code 1.
   Compile this program to `/home/user/health_monitor` using `gcc`.

3. **Staged Deployment Script**:
   Write a bash script at `/home/user/deploy.sh` that simulates a rolling deployment. The script must:
   - Start a dummy background process listening on the port specified in the transcript (e.g., using `nc -l -p <port> &`).
   - Call `/home/user/health_monitor <port> <timeout>` to verify the service is up.
   - If healthy, append "DEPLOYMENT SUCCESS" to `/home/user/deploy.log`.
   - If unhealthy, append "DEPLOYMENT FAILED" to `/home/user/deploy.log`.

Execute your deployment script so that the log file is generated. Ensure all files are in the exact specified paths.