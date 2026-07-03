You are taking over the maintenance of a custom voice-transcription pipeline running entirely in user-space. The system consists of a Python-based API backend, a local Nginx reverse proxy, and a set of automated tasks, but the previous administrator left it in a broken state.

You need to resolve several system administration issues and then use the pipeline to process an incoming audio file.

Here are your tasks:

1. **Fix the Reverse Proxy:**
   There is a user-space Nginx configuration located at `/home/user/nginx.conf` that listens on port `8080`. Currently, any request to `http://127.0.0.1:8080/upload` returns a `502 Bad Gateway` error. The upstream socket path in the configuration is incorrectly pointing to `/home/user/tmp/wrong.sock`. Update the configuration so it correctly points to the backend socket at `/home/user/api.sock`. Restart or reload the nginx process as needed (it runs under the current user, not root).

2. **Configure Locale and Timezone for the Backend:**
   The backend API is started using the script `/home/user/start_backend.sh`. It currently fails to parse some timestamps correctly because it relies on specific regional settings. Modify `/home/user/start_backend.sh` to export the environment variables `TZ` set to `Europe/Paris` and `LC_ALL` set to `fr_FR.UTF-8` before the python application starts. After fixing it, ensure the backend process is running.

3. **Configure a Scheduled Task:**
   To prevent disk space exhaustion, create a script at `/home/user/cleanup.sh` that deletes any `.tmp` files older than 2 days in `/home/user/`. Then, configure a user crontab to execute `/home/user/cleanup.sh` exactly at the top of every hour (minute 0).

4. **Process the Audio Artefact:**
   You have been provided with an audio file at `/app/voicemail.wav`. To save bandwidth and optimize for voice, write a shell script or command using `ffmpeg` to process this file with the following specifications:
   - Resample the audio to 8000 Hz.
   - Mix down to 1 channel (mono).
   - Apply a lowpass audio filter at 3000 Hz.
   Save the resulting processed file exactly to `/home/user/processed_audio.wav`.

5. **Test the Pipeline:**
   Once your Nginx config and backend are running, and your audio is processed, use `curl` to `POST` the `/home/user/processed_audio.wav` file to `http://127.0.0.1:8080/upload` (send it as binary data or form-data, the API accepts standard file uploads). Save the HTTP response body to `/home/user/api_response.txt`.

Ensure all background services are running properly and your final processed audio file exists.