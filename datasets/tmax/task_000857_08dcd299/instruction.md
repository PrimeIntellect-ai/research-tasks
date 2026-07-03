You are an IT support technician responding to Ticket #8912.

**Ticket Description:**
"The internal audio-ticket processor service went down. The original developer left the company and the source code in `/app/ticket-service` currently does not compile. Furthermore, we lost the API key required to run the service, though we know it was accidentally committed to the git repository at some point before being removed. Lastly, the service requires a backup authorization code to process requests. A user left a voice memo with this exact code, which is saved at `/app/ticket_audio.wav`.

Your tasks are:
1. **Git Forensics:** Find the lost API key in the git history of `/app/ticket-service`.
2. **Audio Transcription:** Listen to or transcribe the audio file at `/app/ticket_audio.wav` to recover the spoken backup authorization code.
3. **Code Debugging & Repair:** Fix the build failure in the Go application located in `/app/ticket-service`. There is a syntax error preventing compilation, and a logical bug in `parser.go` where it incorrectly parses incoming ticket dates (format parsing edge-case). The date format expected by clients is `YYYY/MM/DD HH:MM:SS`.
4. **Service Deployment:** Run the compiled Go service. It must listen for HTTP requests on `127.0.0.1:8080`.
   - You must pass the recovered API key as an environment variable named `API_KEY`.
   - The service exposes a `POST /auth` endpoint.

Once the service is running, an automated verifier will send a `POST` request to `http://127.0.0.1:8080/auth` with the following JSON payload:
`{"ticket_date": "2023/10/05 14:30:00", "code": "<the exact authorization code transcribed from the audio>"}`

You must leave the service running in the background listening on `127.0.0.1:8080` so the verifier can test it. Ensure your fixed Go code properly responds with HTTP 200 and `{"status": "authenticated"}` when the correct API key is in the environment and the correct authorization code is provided in the parsed request.