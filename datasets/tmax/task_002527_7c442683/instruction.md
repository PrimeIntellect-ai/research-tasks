**TICKET ID: IT-9042 - Urgent Escalation**

We have an urgent ticket regarding our internal Go-based Voicemail Processing API. It is currently failing to build due to dependency conflicts, and even when it did run, it deadlocked under high contention while trying to process audio files. Additionally, the original developer left and removed the API authorization token from the current repository state, but we know it's buried somewhere in the git history.

Your tasks:
1. Navigate to `/home/user/voicemail-api`. Resolve the Go module dependency conflicts (specifically between the conflicting versions of our internal logger and the audio processing stub).
2. Perform git forensics to recover the API authorization token. The token was hardcoded in an older commit before being replaced with an env var lookup. Save the exact token string into `/home/user/token.txt`.
3. Fix the concurrency bug in `processor.go` that causes a deadlock when multiple goroutines attempt to update the transcription status simultaneously.
4. Start the service on exactly `127.0.0.1:8080`. It must stay running in the background.
5. Our automated verifier will send HTTP requests to test the service. The service must accept HTTP POST requests to `/api/v1/transcribe`, requiring an `Authorization: Bearer <recovered_token>` header, and process audio data sent in the request body. 

There is an emergency voicemail located at `/app/voicemail.wav`. Use the service to process this file and write the resulting transcription string exactly to `/home/user/transcript.log`.