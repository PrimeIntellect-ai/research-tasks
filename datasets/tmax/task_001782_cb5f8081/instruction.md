You are the site administrator for a platform where users upload voice memos for their profiles. You are taking over from a previous admin who left things in a somewhat broken state. 

Your tasks are:

1. **Fix the Health Check Automation:**
   There is a health and connectivity check script at `/home/user/scripts/health_check.sh` that is scheduled to run every minute via cron. The script is supposed to check disk quotas and ping our internal API, logging the results to `/home/user/logs/health.log`. However, due to missing environment variables and PATH differences in the cron environment, it is currently dumping its output into `/home/user/fallback.log` and failing to locate necessary executables. Fix the user's crontab so that the script executes correctly, finds the right path for binaries, and logs successfully to `/home/user/logs/health.log`. 

2. **Recover the Administrator's Instructions:**
   The previous admin left a recorded handover message at `/app/admin_voicemail.wav`. You will need to transcribe the spoken audio in this file (using available command-line tools like `whisper-cpp` or `ffmpeg` to process it if needed) to discover the exact technical criteria for identifying "malicious" user uploads that are bypassing our disk quota monitors.

3. **Develop a Rust-based Audio Sanitizer:**
   Based on the criteria you transcribe from the voicemail, create a Rust command-line application in `/home/user/audio_filter/`. 
   - The application must accept a single argument: the absolute path to a WAV file.
   - It must analyze the file's metadata/headers.
   - It must exit with code `0` if the file is safe (clean).
   - It must exit with code `1` if the file violates the criteria mentioned in the voicemail (evil).

4. **Verify Your Classifier:**
   We have staged a set of historical uploads for you to test your program against.
   - Valid uploads are located in `/app/corpus/clean/`.
   - Known malicious/quota-busting uploads are located in `/app/corpus/evil/`.
   Your Rust program must correctly classify 100% of both directories. 

Compile your Rust program so that the binary is available at `/home/user/audio_filter/target/release/audio_filter`. Leave the cron job running and the Rust binary compiled.