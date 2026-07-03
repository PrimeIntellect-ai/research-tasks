You are acting as a cloud architect migrating an internal audio-authentication microservice to a new environment. 

We have two services managed by a custom shell-based supervisor script located at `/home/user/start_services.sh`.
1. **Service A (Transcription Worker):** A script at `/home/user/worker.sh` that processes an audio file located at `/app/auth_audio.wav` using `whisper-cli` (or similar tools installed in the environment), extracts the spoken passcode, and writes it to `/home/user/config/passcode.txt`.
2. **Service B (Auth API):** A simple HTTP server script at `/home/user/api.sh` that binds to `127.0.0.1:8080`. It reads the passcode from `/home/user/config/passcode.txt` and requires it as a Bearer token for the `/verify` endpoint.

Currently, the migration is failing because of two issues:
1. **Dependency/Race Condition:** `/home/user/start_services.sh` starts both services simultaneously. Service B crashes or serves errors because `/home/user/config/passcode.txt` isn't created yet by Service A. You must fix `/home/user/start_services.sh` so that Service B waits for Service A to successfully write the passcode file before starting.
2. **Permissions:** The `/home/user/config` directory has restrictive permissions. You must configure filesystem ACLs (using `setfacl`) so that the script running Service B has explicit read access to the directory and any files created within it, without changing the standard Unix owner/group permissions of the directory.

Your task:
1. Extract the spoken passcode from `/app/auth_audio.wav` by successfully running the worker (or manually extracting it using available tools if you prefer, but the automated pipeline requires the worker script to succeed).
2. Fix the dependency issue in `/home/user/start_services.sh`.
3. Set the appropriate ACLs on `/home/user/config`.
4. Ensure the services are running in the background and Service B is listening on `127.0.0.1:8080`.
5. Write the final operational logs of both services to `/home/user/migration.log` (format: `[Service A|B] <status>`).

When you have finished, leave the services running. Our automated verification system will issue an HTTP GET request to `http://127.0.0.1:8080/verify` using the transcribed passcode as the Bearer token.