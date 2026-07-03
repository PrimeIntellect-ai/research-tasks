You are an infrastructure engineer tasked with deploying a secure, hardened monitoring API for a storage system. The system must verify authentication using a secret passphrase, calculate storage metrics on a highly restricted directory structure, and serve the results via an HTTP API. 

Follow these requirements precisely:

1. **Authentication Token Recovery**
   The lead administrator left the new API passphrase in an audio recording located at `/app/voicemail.wav`. You must transcribe the contents of this audio file (you may install tools like `openai-whisper`, `ffmpeg`, or `SpeechRecognition` in your local environment). Extract the spoken phrase. The passphrase for the API will be the exact transcribed phrase, converted to all lowercase, with no punctuation.

2. **Storage and Permission Hardening**
   - Create a directory structure starting at `/home/user/vault/data`.
   - Inside `/home/user/vault/data`, create three files: `chunk1.dat` (exactly 1024 bytes), `chunk2.dat` (exactly 2048 bytes), and `chunk3.dat` (exactly 4096 bytes). You can use `/dev/urandom` or `/dev/zero` to generate these.
   - Set the permissions of the `/home/user/vault` directory to strictly `0700` so only the current user can access it.
   - Create a symbolic link at `/home/user/vault/active_data` that points to `/home/user/vault/data`.

3. **Application-Level User ACL**
   - Since we cannot manage system-level users, create an application-level ACL file at `/home/user/vault/app_users.conf`.
   - Use text processing to insert exactly this line into the file, simulating a standard passwd format: `api_admin:x:1001:1001:API Administrator:/home/user/vault:/bin/false`.
   - Restrict this file's permissions to `0400`.

4. **Monitoring Service Configuration**
   - Write and launch an HTTP server (using Python or Node.js) that listens on `127.0.0.1:8123`.
   - The server must implement a `GET /metrics` endpoint.
   - The endpoint must require an HTTP header named `X-Vault-Auth`. If the header is missing or does not exactly match the lowercase passphrase from the audio file, the server must return an HTTP `401 Unauthorized`.
   - If the authentication is successful, the server must dynamically calculate the total size (in bytes) of all files within the directory referenced by the `/home/user/vault/active_data` symlink.
   - The server must return an HTTP `200 OK` with the following JSON payload:
     `{"status": "secure", "total_bytes": <calculated_size_integer>, "acl_present": <boolean_if_app_users.conf_exists>}`
   
Ensure the service remains running in the background on port 8123 so that the automated verification system can issue requests against it.