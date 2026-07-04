You are a FinOps analyst tasked with optimizing and securing a new cloud deployment. Our cloud vendor recently left a voicemail regarding the deployment's storage constraints and process supervision requirements. Additionally, we've had issues with deployment scripts silently injecting SSH configurations that break key-based logins, leading to expensive lockouts.

You must complete the following workflow:

1. **Information Extraction (Audio)**
   Transcribe the vendor's voicemail located at `/app/vendor_call.wav`. The audio contains two critical pieces of information:
   - A specific disk quota size (in megabytes).
   - A specific systemd restart policy.

2. **Disk Quota Monitoring Script**
   Write a Python script at `/home/user/disk_monitor.py` that monitors the directory `/home/user/data`. 
   - The script must calculate the total size of all files in `/home/user/data`.
   - If the total size strictly exceeds the disk quota specified in the voicemail, the script must print exactly `QUOTA_EXCEEDED` to standard output and exit with status code `1`.
   - If the size is within the quota, it must print exactly `OK` and exit with status code `0`.
   - Ensure the script is executable.

3. **Process Supervision Configuration**
   Create a systemd user service unit file at `/home/user/.config/systemd/user/disk-monitor.service`.
   - The `ExecStart` must point to your `/home/user/disk_monitor.py` script.
   - The `Restart` directive in the `[Service]` section must be set exactly to the restart policy mentioned in the voicemail.
   - You do not need to start or enable the service, just create the valid unit file.

4. **SSH Configuration Sanitizer (Adversarial Corpus)**
   We need an automated way to prevent malicious or malformed SSH configs from breaking our server access. Write a Python script at `/home/user/ssh_filter.py` that takes a single command-line argument: the path to an SSH configuration file.
   - The script must parse the provided SSH config.
   - It must detect any configuration that "silently rejects key-based login". Specifically, it must reject the file if it contains directives equivalent to:
     - `PubkeyAuthentication no`
     - `AuthorizedKeysFile /dev/null`
   - If the config is "clean" (safe for key-based login), the script must exit with status code `0`.
   - If the config is "evil" (rejects key-based login), the script must exit with status code `1`.
   - Ignore case and whitespace variations in the SSH directives.

Note: You can use any Python libraries pre-installed or install them via pip. For audio transcription, you may want to use `openai-whisper` or standard `ffmpeg` combined with `SpeechRecognition`.