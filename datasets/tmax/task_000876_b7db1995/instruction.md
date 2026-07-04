You are an artifact manager AI responsible for curating binary repositories. We have received a batch of archived binaries in `/app/incoming/`, but some of the archives were corrupted during transfer. 

Additionally, the release instructions were sent as a voice memo located at `/app/voicemail.wav`. You will need to transcribe this audio file (you may use `whisper` or python's `SpeechRecognition` library, which you can install) to retrieve two critical pieces of information: the exact name of the target release directory, and the TCP port number on which to serve the files.

Perform the following operations:
1. Listen to/transcribe `/app/voicemail.wav` to find the target release directory name and the service port number.
2. Create the target release directory under `/app/`.
3. Verify the integrity of all `.tar.gz` archives in `/app/incoming/`. Discard any archives that are corrupted or fail integrity checks.
4. Extract the contents of the valid archives into a temporary directory.
5. Bulk rename all extracted files: change their extension from `.dat` to `.bin`.
6. Move the renamed files into the target release directory.
7. Generate a manifest file named `SHA256SUMS` inside the release directory containing the SHA256 checksums of all `.bin` files. You MUST use an atomic write pattern (write to a temporary file first, then atomically move it to `SHA256SUMS`) to prevent partial reads by clients.
8. Create a symbolic link named `latest.bin` inside the release directory that points to the largest `.bin` file. If there is a tie, choose the one that comes first alphabetically.
9. Finally, start a background HTTP server (e.g., using `python3 -m http.server`) listening on all interfaces (`0.0.0.0`) on the port specified in the audio, serving the target release directory. Keep the server running.

Your final state should have the HTTP server active so that a client can fetch `SHA256SUMS` and `latest.bin`.