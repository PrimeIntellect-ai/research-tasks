We have a local, user-level systemd service that is supposed to transcribe customer voicemail audio files automatically, but it is currently failing to start and constantly crashing. 

The service is defined at `/home/user/.config/systemd/user/voicemail-transcriber.service`. It relies on a bash script located at `/home/user/transcribe.sh` which processes an incoming audio file located at `/app/voicemail.wav`.

Your task is to diagnose and fix the system setup so that the service runs successfully and generates the correct transcription. Specifically:

1. **Process Supervision & Restart Policies:** The service currently fails to start or gets stuck in a restart loop. Diagnose the `systemctl --user` status and journal logs to find out why. Fix the service definition. It must have a proper restart policy (e.g., restarting on failure with a 5-second delay) and avoid triggering systemd's start limit bursts incorrectly.
2. **Permission & ACL Management:** The script attempts to write logs to `/home/user/logs/transcriber/` and the final output to `/home/user/processed/transcript.txt`. However, there are permission issues. Ensure the directories exist, have the correct permissions (the script needs write access), and ensure standard output/error from the service are properly routed to a log file (`/home/user/logs/transcriber/service.log`).
3. **Log Configuration & Rotation:** Configure a `logrotate` rule in `/home/user/logrotate.conf` to rotate `/home/user/logs/transcriber/service.log` daily, keeping 7 backups, and compressing them. 
4. **Fixing the Transcription Logic:** The script uses a local installation of `whisper-cli` (or a python equivalent available in the environment) to transcribe the audio. You need to ensure the audio processing works. The final text must be written to `/home/user/processed/transcript.txt`. Strip out timestamps and output just the text.

Once you have fixed the script, permissions, and the systemd service file, reload the systemd user daemon, enable, and start the `voicemail-transcriber.service`. Wait for it to finish processing `/app/voicemail.wav`. 

The quality of your final system setup will be verified by checking if the service is actively running/completed without failure, the logs are rotating correctly, and the generated transcript (`/home/user/processed/transcript.txt`) accurately reflects the audio content.