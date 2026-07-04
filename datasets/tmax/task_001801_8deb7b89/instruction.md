You are tasked with automating a legacy interactive transcription pipeline and securely serving the output. A recent network configuration change broke our internal Docker routing, so we are moving the processing locally to a single node.

We have an audio file located at `/app/voicemail.wav`.
There is an interactive tool located at `/app/interactive_transcriber` (a compiled binary from C, but you only have the binary and must wrap it) that processes audio files. However, it requires interactive input at runtime.

Your requirements:
1. Write an `expect` script at `/home/user/automate.exp` that runs `/app/interactive_transcriber`. The interactive transcriber prompts exactly:
   - "Enter path to audio file: "
   - "Enter output text file path: "
   Make it save the output to `/home/user/transcript.txt`.
2. Write a lightweight C program at `/home/user/server.c` that, when compiled to `/home/user/server` and run, binds to port 8443 and serves the contents of `/home/user/transcript.txt` over HTTPS. You must generate your own self-signed certificates (`/home/user/cert.pem` and `/home/user/key.pem`) and use OpenSSL in your C code to handle the TLS layer. 
3. Run your C server in the background so that a GET request to `https://127.0.0.1:8443/` returns the transcript.

An automated test will use `curl -k https://127.0.0.1:8443/` to fetch the text. Ensure the text response contains the transcribed spoken content with high accuracy.