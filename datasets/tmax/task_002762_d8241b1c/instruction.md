We have a user-level systemd service called `voicemail-api.service` that keeps failing to start. It is designed to act as a dual-protocol backend (HTTP and gRPC) that serves the transcription of a highly critical voicemail file located at `/app/voicemail.wav`. 

Your objective is to diagnose the failure, fix the configuration, and successfully launch the service so it can be queried securely.

Here are the requirements to complete the task:
1. **Locale and Timezone Fix**: The service crashes because it strictly requires its environment to run in the `Europe/Zurich` timezone and the `fr_CH.UTF-8` locale. You must configure the user systemd service to inject these specific environment variables.
2. **Audio Transcription**: Transcribe the audio file located at `/app/voicemail.wav`. The Python service script (`/home/user/app/server.py`) is missing the hardcoded transcription. You must recover the spoken content from the WAV file and update the `TRANSCRIPT_TEXT` variable in the Python script.
3. **Service Management**: Fix any pathing or configuration issues in `~/.config/systemd/user/voicemail-api.service` and start it successfully using `systemctl --user start voicemail-api`.
4. **SSH Tunneling**: The service binds HTTP to `localhost:8080` and gRPC to `localhost:50051`. However, our automated verifier requires secure access to the HTTP endpoint via port `9090`. You must set up a local SSH port forward that maps `localhost:9090` to the service's HTTP port (`8080`).

The verifier will test your setup by:
- Sending an HTTP GET request to `http://localhost:9090/transcript` with the header `Authorization: Bearer voicemail-admin`. It expects a JSON response: `{"transcript": "<exact_audio_transcript>", "tz": "Europe/Zurich", "locale": "fr_CH.UTF-8"}`.
- Making a gRPC call to `localhost:50051`. 

Ensure all configurations are saved, the service is permanently running, and the SSH tunnel is active.